# Containers Specification

## Container Types

### Group (`group;container=1;`)

Groups visually cluster cells. They must have `container=1`.
Groups without `container=1` receive a WARNING.

Edges should not connect directly to group cells — connect to children instead.

### Swimlane (`swimlane;startSize=30;`)

Swimlanes must specify `startSize` for the header bar height.
Missing `startSize` causes a WARNING.

### Custom Container (`container=1;`)

Custom containers should include `pointerEvents=0` to prevent
the container from capturing click events meant for children.

## Children Bounds (SHOULD)

Child cells should not extend beyond parent container bounds.

## Collapsible (INFO)

Consider adding `collapsible=1` for interactive containers.

## Validation Mode

- Pointer events: **STANDARD**
- Children bounds: **STANDARD**
- Swimlane startSize: **STANDARD**
- Collapsible: **STANDARD**
- Group detection: **STRICT**
- Group connectability: **STRICT**
