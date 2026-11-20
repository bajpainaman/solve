// Source read at: 0000000
// Covers: examples/bad/shadowed-permit/ (this example describes no real
// repository, so the commit is a placeholder)

// A high-clearance user should still be able to view a secret document in
// their own department.
permit(
  principal,
  action == Action::"viewDocument",
  resource
) when {
  principal.department == resource.owningDepartment &&
  resource.classification == "secret" &&
  principal.clearance == "high"
};

permit(
  principal,
  action == Action::"viewDocument",
  resource
) when {
  principal.department == resource.owningDepartment &&
  resource.classification != "secret"
};

// Meant to block a low-clearance user from a secret document, but the
// condition forbids every secret document, high clearance included, so it
// shadows the permit above for every high-clearance user too.
forbid(
  principal,
  action == Action::"viewDocument",
  resource
) when {
  resource.classification == "secret"
};
