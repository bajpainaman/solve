Review as a red team of two attackers and one defender. The first attacker
looks for ways an unauthenticated caller can reach data or actions they
shouldn't. The second attacker looks for ways an authenticated user can act as
another user or another tenant. Both trace every changed input from where it
enters the system to where it's stored, logged or sent onward. The defender then
reviews the attackers' output, drops any attack that the code or its framework
already blocks, and confirms that each remaining issue is reachable. Ignore
performance and style unless they open an attack.
