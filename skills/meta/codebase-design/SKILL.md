---
name: codebase-design
description: Use when shaping module interfaces, placing seams, deepening shallow code, or making code more testable, local, and AI-navigable.
---

# Codebase Design

Design deep modules: small interfaces that hide meaningful behavior at clean seams, creating leverage for callers and locality for maintainers.

## Core Vocabulary

Use these terms consistently:

- **Module**: anything with an interface and implementation.
- **Interface**: everything a caller must know to use the module correctly.
- **Implementation**: the code hidden behind the interface.
- **Depth**: leverage at the interface; more behavior per unit of surface.
- **Seam**: the place where behavior can vary without editing the caller.
- **Adapter**: a concrete implementation that satisfies an interface at a seam.
- **Leverage**: repeated payoff for callers and tests.
- **Locality**: change and verification concentrated in one place.

## Workflow

1. Name the module, its callers, and the behavior the interface should hide.
2. Apply the deletion test: if deleting it only moves pass-through code, it is shallow.
3. Place seams only where behavior genuinely varies or testing needs a stable interface.
4. Make the interface the test surface; avoid testing through private implementation detail.
5. Compare alternatives when the seam is consequential.

## Supporting Material

- Read `references/deep-module-vocabulary.md` for the full vocabulary, principles, diagrams, and examples.
- Read `references/deepening.md` when deepening an existing cluster.
- Read `references/design-it-twice.md` when comparing multiple interface designs.
