export type Variant = 'surface' | 'outline' | 'subtle';
export type Tone = 'neutral' | 'primary' | 'success' | 'warning' | 'danger' | 'info';
export type Size = 'sm' | 'md' | 'lg';
export type Radius = 'lg' | 'xl' | '2xl';
export type Elevation = 'none' | 'sm' | 'md' | 'lg';
export type Hoverable = boolean;
export type Highlighted = boolean;

// Arrays for Storybook controls
export const VARIANTS: Variant[] = ['surface', 'outline', 'subtle'];
export const TONES: Tone[] = ['neutral', 'primary', 'success', 'warning', 'danger', 'info'];
export const SIZES: Size[] = ['sm', 'md', 'lg'];
export const RADII: Radius[] = ['lg', 'xl', '2xl'];
export const ELEVATIONS: Elevation[] = ['none', 'sm', 'md', 'lg'];
