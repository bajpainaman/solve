-- Source read at: 0000000
-- Covers: authz/namespace.py
--
-- The header shows the form of a sync record. This example describes no real
-- repository, so the commit is a placeholder.
--
-- Relationship-based access control, in the shape Zanzibar calls a namespace
-- config. An object sits under at most one parent object, such as a document
-- inside a folder. A user can be granted viewer or editor directly on an
-- object. A rewrite rule computes who else holds a permission by inheriting
-- it down the parent chain.

sig User {}
sig Object {
  parent: lone Object,  -- the folder a document sits in, or none for a folder at the top
  viewer: set User,     -- users granted viewer directly on this object
  editor: set User      -- users granted editor directly on this object
}

-- True by construction: the containment graph the service stores has no cycle.
fact Acyclic { no o: Object | o in o.^parent }

-- Source: namespace.py, the "editor" rewrite rule in the intended config:
-- editor of an object, or editor of any ancestor, computed along parent.
fun editorsViaEditorChain[o: Object]: set User { o.*parent.editor }

-- Source: namespace.py, a second copy of the rule that unions in the
-- "viewer" relation of each ancestor as well. A namespace config edited to
-- add a rewrite rule can union the wrong relation into another by mistake.
fun editorsViaEditorOrViewerChain[o: Object]: set User { o.*parent.editor + o.*parent.viewer }

-- "A user with editor access on an object was granted editor somewhere on
-- its ancestor chain, including the object itself." Checked once per
-- rewrite rule, so a grant of viewer on an ancestor confers nothing beyond
-- viewing only when the rule that computes editors is the editor-only chain.
assert NoUnintendedEditFromAncestorViewer_EditorChain {
  no u: User, o: Object | u in editorsViaEditorChain[o] and u not in o.*parent.editor
}
-- The rejected rewrite rule: the same claim, computed with the rule that
-- also inherits from viewer grants on an ancestor.
assert NoUnintendedEditFromAncestorViewer_EditorOrViewerChain {
  no u: User, o: Object | u in editorsViaEditorOrViewerChain[o] and u not in o.*parent.editor
}

-- Witness: inheritance actually hands a user editor rights on a descendant
-- they were never granted it on directly.
pred SomeoneInheritsEditFromAnAncestor {
  some u: User, o: Object | u in editorsViaEditorChain[o] and u not in o.editor and some o.parent
}

-- Witness for the rejected rule: a user who only views a folder ends up with
-- the editor rewrite on a document inside it.
pred ViewerOfFolderGrantsEditOnChild {
  some u: User, folder, doc: Object |
    doc.parent = folder and u in folder.viewer and
    u in editorsViaEditorOrViewerChain[doc] and u not in doc.*parent.editor
}

run SomeoneInheritsEditFromAnAncestor for 4 expect 1
run ViewerOfFolderGrantsEditOnChild for 4 expect 1
check NoUnintendedEditFromAncestorViewer_EditorChain for 4 expect 0
check NoUnintendedEditFromAncestorViewer_EditorOrViewerChain for 4 expect 1
