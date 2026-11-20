// Source read at: 0000000
// Covers: examples/good/document-access/ (this example describes no real
// repository, so the commit is a placeholder)

// A user may view a document owned by their own department.
permit(
  principal,
  action == Action::"viewDocument",
  resource
) when {
  principal.department == resource.owningDepartment
};

// A secret document stays forbidden to anyone without high clearance, even
// inside the owning department.
forbid(
  principal,
  action == Action::"viewDocument",
  resource
) when {
  resource.classification == "secret" && principal.clearance != "high"
};
