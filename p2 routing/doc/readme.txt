EE-122 Network Simulator
------------------------


File Layout
-----------
The simulator is organized thusly:
simulator.py - Starts up the simulator.
sim/core.py - Inner workings of the simulator.  Keep out.
sim/api.py - Parts of the simulator that you'll need to use (such as the Entity
             class).  See help(api).
sim/basics.py - Basic simulator pieces build with the API, such as a Hub
                Entity.  See help(basics).
sim/topo.py - You can use this to create your own topologies/scenarios.  See
              help(topo).
scenarios/*.py - Test topologies and scenarios for you to use.  See
                 help(scenarios).
tests/*.py - Automated test case examples, including compatibility test.


Getting Started
---------------
To start the simulator, run simulator.py:

    $ python simulator.py

This spouts some informational text, and gives you a Python interpreter.  From
the interpreter, you can run arbitrary Python code, can inspect and manipulate
the simulation, and can get help on many aspects of the simulator.

As simulator.py comes, it simply creates a test scenario (mostly this just
means a topology) and starts the simulator.  You may wish to modify it to load
a different scenario (including a custom one). If you want to change scenarios,
you'll need to restart simulator.py.

The scenarios in the scenario directory each contain a create() method.  You
might want to look at these.  They create the topology that goes with the
scenario.  The included ones can be run with an arbitrary switch class, so you
can easily set them up using a hub, a leaning switch, your RIP-like switch,
etc.).

From the simulator's commandline, you have access to all the Entities created
in your scenario, and you can interact with these.  For example:

    >>> h1.ping(h2)


Implementing Entities
---------------------
Objects that exist in the simulator are subclasses of the Entity superclass (in
api.py).  These have a handful of utility functions, as well as some empty
functions that are called when various events occur.  You probably want to
handle at least some of these events!  For more help try help(api.Entity)
within the simulator.


Sending Packets
---------------
Entities can send and receive packets.  In the simulator, this means a subclass
of Packet.  See basics.Ping for one such example, and see basics.BasicHost to
see an example of how it is used.


Building Your Own Scenarios
---------------------------
You may want to test using your own topologies, and you may want to test your
own events (such as nodes joining and leaving the network) within those
topologies.  We refer to the combination of those as a "scenario".  The
simulator should come with some (in the scenarios directory) to get you
started, but you may want to build your own.  To start:

    >>> import sim.topo as topo

The first step is simply creating some Entities so that the simulator can use
them.  You shouldn't create the nodes yourself, but rather let the
CreateEntity() function in core do it for you, something along the lines of:

    >>> CreateEntity('myNewNode', MyNodeType, arg1, arg2)

That is, you *don't* want to use normal Python object creation like:

    >>> x = MyNodeType(arg1, arg2) # Don't do this

CreateEntity() returns the new entity, and all entities that you create are
added to the sim package.  So you can do:

    >>> import sim
    >>> x = CreateEntity('myNewNode', MyNodeType, arg1, arg2)
    >>> print sim.myNewNode, x

.. which will show the new Entity twice.

To link this to some other Entity:

    >>> topo.link(sim.myNewNode, sim.someOtherNode)

You can also unlink it, or disconnect it from everything:

    >>> topo.disconnect(sim.myNewNode)

To see the connections on a given Entity:

    >>> topo.show_ports(sim.someNode)

.. this shows how the ports on someNode are connected to other nodes and their ports.


Writing Tests
-------------
Since you can create your own custom topologies, it's easy to write your own
test cases; we don't provide a "test framework" per se for this assignment. We
do provide one test case that is very similar to one of the actual grading test
cases to give you an idea of how you might write an automated test case for
your submission. You can run a test by entering at your command prompt (*not*
in simulator.py):

    $ python tests/<test case>.py

VERY IMPORTANT: We also include a stand-alone "compatibility test"
(tests/compat_test.py) in the test case folder. Your submission MUST pass this
test before you submit it to ensure we'll be able to grade it. Submissions that
fail this test will receive a score of zero!
