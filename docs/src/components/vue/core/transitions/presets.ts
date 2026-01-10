/**
 * Transition preset definitions for Headless UI components
 * 
 * These presets provide consistent, accessible animations across the design system.
 * All presets include reduced motion support via Tailwind's motion-reduce variants.
 * 
 * Usage with Headless UI TransitionChild:
 * ```vue
 * <TransitionChild v-bind="fadeScaleSm" as="template">
 *   <DialogPanel>...</DialogPanel>
 * </TransitionChild>
 * ```
 */

export type TransitionPreset = {
  enter: string
  enterFrom: string
  enterTo: string
  leave: string
  leaveFrom: string
  leaveTo: string
}

/**
 * Simple fade in/out
 * Best for: backdrops, overlays
 */
export const fade: TransitionPreset = {
  enter: 'transition-opacity duration-150 ease-out motion-reduce:transition-none',
  enterFrom: 'opacity-0',
  enterTo: 'opacity-100',
  leave: 'transition-opacity duration-100 ease-in motion-reduce:transition-none',
  leaveFrom: 'opacity-100',
  leaveTo: 'opacity-0'
}

/**
 * Fade + subtle scale (95-100%)
 * Best for: Dialog/Modal panels, Popover content (default choice)
 */
export const fadeScaleSm: TransitionPreset = {
  enter: 'transition-all duration-150 ease-out motion-reduce:transition-none motion-reduce:transform-none',
  enterFrom: 'opacity-0 scale-95',
  enterTo: 'opacity-100 scale-100',
  leave: 'transition-all duration-100 ease-in motion-reduce:transition-none motion-reduce:transform-none',
  leaveFrom: 'opacity-100 scale-100',
  leaveTo: 'opacity-0 scale-95'
}

/**
 * Fade + stronger scale (90-100%)
 * Best for: emphasis animations, special modals
 */
export const fadeScaleMd: TransitionPreset = {
  enter: 'transition-all duration-200 ease-out motion-reduce:transition-none motion-reduce:transform-none',
  enterFrom: 'opacity-0 scale-90',
  enterTo: 'opacity-100 scale-100',
  leave: 'transition-all duration-150 ease-in motion-reduce:transition-none motion-reduce:transform-none',
  leaveFrom: 'opacity-100 scale-100',
  leaveTo: 'opacity-0 scale-90'
}

/**
 * Slide down from top
 * Best for: dropdown menus, select options
 */
export const slideDownSm: TransitionPreset = {
  enter: 'transition-all duration-150 ease-out motion-reduce:transition-none motion-reduce:transform-none',
  enterFrom: 'opacity-0 -translate-y-2',
  enterTo: 'opacity-100 translate-y-0',
  leave: 'transition-all duration-100 ease-in motion-reduce:transition-none motion-reduce:transform-none',
  leaveFrom: 'opacity-100 translate-y-0',
  leaveTo: 'opacity-0 -translate-y-2'
}

/**
 * Slide up from bottom
 * Best for: toasts, bottom sheets, notifications
 */
export const slideUpSm: TransitionPreset = {
  enter: 'transition-all duration-150 ease-out motion-reduce:transition-none motion-reduce:transform-none',
  enterFrom: 'opacity-0 translate-y-2',
  enterTo: 'opacity-100 translate-y-0',
  leave: 'transition-all duration-100 ease-in motion-reduce:transition-none motion-reduce:transform-none',
  leaveFrom: 'opacity-100 translate-y-0',
  leaveTo: 'opacity-0 translate-y-2'
}

/**
 * Slide in from left
 * Best for: slide-over panels from left edge
 */
export const slideLeftSm: TransitionPreset = {
  enter: 'transition-all duration-200 ease-out motion-reduce:transition-none motion-reduce:transform-none',
  enterFrom: 'opacity-0 -translate-x-4',
  enterTo: 'opacity-100 translate-x-0',
  leave: 'transition-all duration-150 ease-in motion-reduce:transition-none motion-reduce:transform-none',
  leaveFrom: 'opacity-100 translate-x-0',
  leaveTo: 'opacity-0 -translate-x-4'
}

/**
 * Slide in from right
 * Best for: slide-over panels from right edge
 */
export const slideRightSm: TransitionPreset = {
  enter: 'transition-all duration-200 ease-out motion-reduce:transition-none motion-reduce:transform-none',
  enterFrom: 'opacity-0 translate-x-4',
  enterTo: 'opacity-100 translate-x-0',
  leave: 'transition-all duration-150 ease-in motion-reduce:transition-none motion-reduce:transform-none',
  leaveFrom: 'opacity-100 translate-x-0',
  leaveTo: 'opacity-0 translate-x-4'
}

/**
 * No animation
 * Best for: when animations should be disabled
 */
export const none: TransitionPreset = {
  enter: '',
  enterFrom: '',
  enterTo: '',
  leave: '',
  leaveFrom: '',
  leaveTo: ''
}
