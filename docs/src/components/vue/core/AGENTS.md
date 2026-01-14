Things that arent allowed when changing Vue core components.

- When there is a type in docs/src/design-system/tokens.ts and in this component you use a prop with
  the same name you have to use that type!
  For Example not allowed:
  variant?: 'solid' | 'soft' | 'outline'

since there is the type Variant in token.ts, you have to use:

variant?: Variant

or rename the prop to something else;
