=================
Firewall compiler
=================

.. contents::

Overview
========

Firewall-compiler allows you to modularize your netfilter firewall
configuration.  The goal is to be as simple as possible while still
providing a mechanism for individual software packages to describe
their own firewall requirements (and allow the system administrator a
convenient means of enabling and disabling particular firewall
rulesets).

Theory of operation
===================

Examples
========

Enabling ssh access
-------------------

This example demonstrates the basic operation of
``firewall-compiler``.

Create a file in ``/etc/firewall/rules.d`` called ``ssh.rules`` with
the following contents::

  *filter
  -A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT 
  COMMIT

Running ``fwc-list`` will now show this as an available ruleset::

  # fwc-list
    ssh.rules

Enable this ruleset by running::

  # fwc-enable ssh

``fwc-list`` will now show this rule as being active::

  # fwc-list
  * ssh.rules

If you were to generate a new netfilter configuration (assuming you
have made no changes to the default template), your configuration
would look like this::

  # Generated at Mon Oct 25 15:21:45 2010 by fwc.
  # Changes made here will be lost when this file is
  # next generated.

  *nat
  :PREROUTING ACCEPT [0:0]
  :POSTROUTING ACCEPT [0:0]
  :OUTPUT ACCEPT [0:0]
  COMMIT

  *filter
  :INPUT ACCEPT [0:0]
  :FORWARD ACCEPT [0:0]
  :OUTPUT ACCEPT [0:0]

  -A INPUT -i lo -j ACCEPT 
  -A INPUT -p icmp -m icmp --icmp-type any -j ACCEPT 
  -A INPUT -p esp -j ACCEPT 
  -A INPUT -p ah -j ACCEPT 
  -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

  # START OF GENERATED RULES
  -A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT 
  # END OF GENERATED RULES

  # Ignore broadcast and multicast traffic so that we don't
  # clutter our firewall logs with junk.
  -A INPUT -m pkttype --pkt-type multicast -j DROP
  -A INPUT -m pkttype --pkt-type broadcast -j DROP

  # Log and reject everything else.  Limit rate of logged
  # packets to avoid DOS in case of high packet rates.
  -A INPUT -j LOG -m limit --limit 1/s
  -A INPUT -j REJECT --reject-with icmp-host-prohibited 
  COMMIT

A transparent proxy
-------------------

In this example, an system acting as a router will intercept traffic
on port 80 and redirect to local port 3128. Connections from host
192.168.1.10 will not be intercepted.

Create a file in ``/etc/firewall/rules.d`` called ``proxy.rules`` with
the following contents::

  *nat
  -A PREROUTING -s 192.168.1.10 -j ACCEPT
  -A PREROUTING -p tcp -m -state --state NEW --dport 80 -j REDIRECT --to-ports 3128
  COMMIT

  *filter
  -A INPUT -p tcp -m state --state NEW --dport 80 -j ACCEPT 
  -A INPUT -p tcp -m state --state NEW --dport 3128 -j ACCEPT 
  COMMIT

Running ``fwc-list`` will now show this as an available ruleset::

  # fwc-list
    proxy.rules
  * ssh.rules

Enable this ruleset by running::

  # fwc-enable proxy

``fwc-list`` will now show this rule as being active::

  # fwc-list
  * ssh.rules
  * proxy.rules

If you were to generate a new netfilter configuration (assuming you
have made no changes to the default template), your configuration
would look like this::

  # Generated at Mon Oct 25 15:27:49 2010 by fwc.
  # Changes made here will be lost when this file is
  # next generated.

  *nat
  :PREROUTING ACCEPT [0:0]
  :POSTROUTING ACCEPT [0:0]
  :OUTPUT ACCEPT [0:0]

  # START OF GENERATED RULES
  -A PREROUTING -s 192.168.1.10 -j ACCEPT
  -A PREROUTING -p tcp -m -state --state NEW --dport 80 -j REDIRECT --to-ports 3128
  # END OF GENERATED RULES
  COMMIT

  *filter
  :INPUT ACCEPT [0:0]
  :FORWARD ACCEPT [0:0]
  :OUTPUT ACCEPT [0:0]

  -A INPUT -i lo -j ACCEPT 
  -A INPUT -p icmp -m icmp --icmp-type any -j ACCEPT 
  -A INPUT -p esp -j ACCEPT 
  -A INPUT -p ah -j ACCEPT 
  -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

  # START OF GENERATED RULES
  -A INPUT -p tcp -m state --state NEW --dport 80 -j ACCEPT 
  -A INPUT -p tcp -m state --state NEW --dport 3128 -j ACCEPT 
  -A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT 
  # END OF GENERATED RULES

  # Ignore broadcast and multicast traffic so that we don't
  # clutter our firewall logs with junk.
  -A INPUT -m pkttype --pkt-type multicast -j DROP
  -A INPUT -m pkttype --pkt-type broadcast -j DROP

  # Log and reject everything else.  Limit rate of logged
  # packets to avoid DOS in case of high packet rates.
  -A INPUT -j LOG -m limit --limit 1/s
  -A INPUT -j REJECT --reject-with icmp-host-prohibited 
  COMMIT


Author
======

Lars Kellogg-Stedman <lars@oddbit.com>

