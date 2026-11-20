// The rejected design: the forbid rule on secret documents is gone, so a
// low-clearance user in the owning department can view a secret document.
// This is the access widening a schema or policy review must catch.
//
// Source read at: 0000000
// Covers: examples/good/document-access/ (this example describes no real
// repository, so the commit is a placeholder)

permit(
  principal,
  action == Action::"viewDocument",
  resource
) when {
  principal.department == resource.owningDepartment
};
