---
title: "Following the manual was exactly the problem"
date: 2026-09-05
draft: false
tags: ["devops", "security", "compliance", "homelab", "tooling"]
translationKey: "internetnl-selfhosting-traps"
summary: "Internet.nl measures whether your domain has IPv6, DNSSEC, RPKI and TLS right. Doing that for a whole fleet needs the batch API, and the batch API needs an account. You can host it yourself — but one variable in the official manual silently kills all outbound traffic, and the certbot in the image cannot even start, so your certificate expires with nothing raising an alarm. Four traps, with the exact error strings, and what they say about documentation that is technically correct."
---

*Four traps when self-hosting an Internet.nl batch instance — and why
"the documentation is correct" is not the same as "the documentation
helps".*

Internet.nl is one of the more useful public services the Netherlands
runs. You type in a domain and get back whether IPv6, DNSSEC, RPKI, TLS
and your mail security are in order. For government bodies and their
suppliers this is not a vanity score: it feeds into the Dutch
comply-or-explain list, and with NIS2 and the ENISA frameworks on top,
you increasingly have to not just *have* these things right but
*demonstrate* it.

That is where it gets awkward. You do not demonstrate anything with a
screenshot of a website. An auditor asking "how do you know this was also
true last month" gets nothing out of a picture. You want a measurement
that runs every day, a result you can diff, and a pipeline that complains
when your score drops.

All of which is possible, because the batch API exists. It just needs an
account, and not everyone gets one. Which leaves self-hosting. The
documentation for that exists, is thorough, and is correct on every line
I checked.

And still I lost days.

None of what follows is a criticism of the project. Internet.nl is open
source, well maintained, and its Docker deployment is better documented
than most things I meet in production. These are the four places where you
can follow the manual literally and still end up with a broken instance. I
am writing them down with the exact error strings, because that is what you
type into a search engine when you are in the middle of it.

## 1. One variable, two meanings

The batch deployment document says this:

```
INTERNETNL_DOMAINNAME=example.com \
IPV4_IP_PUBLIC=127.0.0.1 \
IPV6_IP_PUBLIC=::1 \
envsubst < docker/host-dist.env > docker/host.env
```

With the explanation: set those public IP variables to loopback, because
that disables the connection-test DNS server, which a batch instance does
not use. That is true. I did it.

Everything came up healthy. Every container `healthy`, not a complaint in
the logs. And every test I submitted failed. The resolver could not
resolve, routinator could not fetch its RPKI data, and nothing on the
`public-internet` network could reach anything at all.

The cause is in `docker/compose.yaml`, in the network block:

```yaml
      # set NAT source IPs to the configured public IPs
      com.docker.network.host_ipv4: $IPV4_IP_PUBLIC
      com.docker.network.host_ipv6: $IPV6_IP_PUBLIC
```

The same two variables. One variable carrying two entirely unrelated
meanings: the address the connection test listens on, *and* the source
address Docker rewrites every outbound packet to. The value that switches
the first one off tells the second one to NAT all your traffic to
`127.0.0.1`.

Once you know, you see it immediately in `iptables -t nat -L POSTROUTING`.
If you do not know, you look in the wrong place, because every symptom
points at DNS.

The fix: put the host's *real* public addresses in `docker/host.env`,
exactly as the non-batch document says, and disable the connection-test DNS
server separately by binding the `UNBOUND_PORT_*` variables to loopback.
Then you have working egress *and* no publicly reachable DNS listener,
which is what the manual was after.

## 2. Certbot cannot start, so your certificate simply expires

This one is quieter and therefore nastier. Your certificate is not renewed,
and you find out when it has expired. The cron inside the container does
run, but produces a Python traceback instead of a renewal:

```
+ /opt/certbot/bin/certbot renew --post-hook 'nginx -s reload'
Traceback (most recent call last):
  File "/opt/certbot/bin/certbot", line 5, in <module>
    from certbot.main import main
  File "/opt/certbot/lib/python3.12/site-packages/certbot/_internal/main.py", line 20, in <module>
    import josepy as jose
  File "/opt/certbot/lib/python3.12/site-packages/josepy/__init__.py", line 41, in <module>
    from josepy.json_util import (
```

It is an incompatibility between the pinned `josepy` and the `pyOpenSSL` in
the image, around the removal of `X509Req`. Repairable inside the
container:

```sh
docker exec internetnl-prod-webserver-1 /opt/certbot/bin/pip install -U certbot josepy
```

But note: that fix lives in the container's writable layer and is gone the
moment the image is updated. Put a reminder on your certificate's expiry
date until upstream ships a fixed image. It is tracked
[as an issue](https://github.com/internetstandards/Internet.nl/issues/2142).

This is exactly why I call running an instance a service rather than a
script. You are not finished when it works.

## 3. The compose wrapper wants a terminal

Everything you do over SSH from a script or a CI job fails, while the
identical command works fine when you are logged in yourself. The wrapper
starts the compose container with a hard-coded `-ti`:

```sh
exec docker run -ti --rm --pull=never \
```

That `-t` wants a terminal, and `ssh host 'command'` does not give it one.
Force one with `ssh -tt`. Two t's, not one: a single `-t` is refused
precisely when stdin is not a terminal, which is the situation you are
trying to fix.

## 4. A recreated network strands the old containers

After a compose run that recreates the network, some containers can no
longer reach each other. They look healthy. They are simply still attached
to a network ID that no longer exists. Restarting does not help, because
they reattach to that same dead ID. Removing and recreating them does:

```sh
docker ps -a --filter status=exited -q | xargs -r docker rm
docker/compose.sh ... up -d
```

## What this says about documentation

I wrote earlier that [stale documentation is worse than no
documentation](/en/posts/2026-07-14-living-documentation-with-gates-and-agents/).
These four cases are a variant that bothers me more: the documentation is
not stale. Every sentence is correct. Trap one is a true statement about
what that variable does — it is just not the whole story, and the missing
half lives in a different file.

That is not a documentation problem you fix by writing better. It is a
design problem that becomes visible in the documentation: a variable that
means two things cannot be honestly explained in one sentence. The manual
is suffering from the code.

The lesson I take from it, and try to hold myself to: if you are writing an
instruction where you cannot say "and this has no other consequences" with a
straight face, that is a signal about your code, not about your prose.

## What I built with it

There is now a chain that hides all of this from anyone who would rather
not deal with it. A self-hosted batch instance on a VPS, reached over a
tailnet, with a facade in front handling tenants, limits and an audit
trail. A CLI and a GitHub Action that fail your build when your score
drops. And a demo where you can type in a domain without an account.

It measures itself every morning, and the result goes up unedited on the
[demo page](https://mwest2020.github.io/internetnl-cli-demo/) — including
the domain that scores markedly worse than the rest. I leave that one up on
purpose: it is deliberately closed to the public, and a scoreboard showing
nothing but green ticks measures nothing.

- **Code, and the four traps written out:**
  [github.com/MWest2020/internetnl-cli](https://github.com/MWest2020/internetnl-cli)
- **Try it, no account needed:**
  [mwest2020.github.io/internetnl-cli-demo](https://mwest2020.github.io/internetnl-cli-demo/)

One house rule, and it applies to you too: only measure hosts you operate
or have explicit permission to test.
