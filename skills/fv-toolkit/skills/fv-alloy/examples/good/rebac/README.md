# Relationship-based access control (Zanzibar-style)

**Pattern:** ReBAC, Zanzibar-style (catalog E).
**Teaches:** a namespace rewrite rule as a function, two rewrite rules checked side by side, a witness, a mutations file.

## The system

An object, such as a document, sits under at most one parent object, such as a folder. A user can be granted viewer or editor directly on an object. A rewrite rule computes who else holds editor by inheriting it down the parent chain, the way a Zanzibar namespace config composes one relation from others.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| A user with editor access was granted editor somewhere on the object's ancestor chain | safety | `NoUnintendedEditFromAncestorViewer_EditorChain` |
| Inheritance actually hands someone editor rights they were not granted directly | reachability | `run SomeoneInheritsEditFromAnAncestor ... expect 1` |
| A viewer of a folder gets the editor rewrite on a document inside it | reachability | `run ViewerOfFolderGrantsEditOnChild ... expect 1` |

## Commands

| Command | Rewrite rule | Expectation |
|---|---|---|
| `run SomeoneInheritsEditFromAnAncestor for 4` | `editorsViaEditorChain` | SAT: inheritance reaches a descendant |
| `run ViewerOfFolderGrantsEditOnChild for 4` | `editorsViaEditorOrViewerChain` | SAT: a folder's viewer ends up with edit on a document inside it |
| `check NoUnintendedEditFromAncestorViewer_EditorChain for 4` | `editorsViaEditorChain` | UNSAT: no counterexample |
| `check NoUnintendedEditFromAncestorViewer_EditorOrViewerChain for 4` | `editorsViaEditorOrViewerChain` | SAT: a counterexample exists |

`editorsViaEditorChain` is the namespace config this project ships: editor rights come only from editor grants on the object or an ancestor. `editorsViaEditorOrViewerChain` is a second copy of the rule with one term changed, the shape of a config edit that unions the wrong relation into another. The last command is the rejected rule. It must find a counterexample. When it stops finding one, the model has lost the ability to show the unintended path.

## Run

```bash
fv-alloy --show rebac.als
fv-mutate rebac.mutations
```

## The counterexample, as the user reads it

```text
this/Object<:parent={Object$1->Object$0}
this/Object<:viewer={Object$0->User$0}
this/Object<:editor={}
```

1. Object 0 is a folder. User 0 holds viewer on it, and nobody holds editor on it.
2. Object 1 is a document whose parent is the folder, Object 0.
3. The editor-or-viewer rewrite rule computes editor rights for the document from editor grants on the chain and viewer grants on the chain.
4. User 0 holds no editor grant anywhere on the chain, yet the rule puts User 0 in the document's computed editors, because the rule also followed the viewer relation.

## Bounds and limits

The checks cover every structure with up to four users and four objects. The model has one relation for containment and two for direct grants. It has no group membership and no revocation.
