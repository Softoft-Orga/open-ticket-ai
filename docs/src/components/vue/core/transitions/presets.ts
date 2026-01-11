/**
 * Transition presets for HeadlessUI TransitionChild components
 * 
 * These presets provide consistent, accessible animations with motion-reduce support.
 * Use with v-bind on TransitionChild components.
 * 
 * @example
 * <TransitionChild v-bind="fade" as="template">
 *   <div>Content</div>
 * </TransitionChild>
 */

/**
 * Simple fade transition
 * Use for: Backdrops, overlays
 */
export const fade = {
  enter: 'transition-opacity duration-300 ease-out',
  enterFrom: 'opacity-0',
  enterTo: 'opacity-100',
  leave: 'transition-opacity duration-200 ease-in',
  leaveFrom: 'opacity-100',
  leaveTo: 'opacity-0'
}

/**
 * Fade with scale transition (small)
 * Use for: Dialogs, modals, popovers
 */
export const fadeScaleSm = {
  enter: 'transition-all duration-300 ease-out motion-reduce:transition-opacity',
  enterFrom: 'opacity-0 scale-95 motion-reduce:scale-100',
  enterTo: 'opacity-100 scale-100',
  leave: 'transition-all duration-200 ease-in motion-reduce:transition-opacity',
  leaveFrom: 'opacity-100 scale-100',
  leaveTo: 'opacity-0 scale-95 motion-reduce:scale-100'
}

/**
 * Fade with scale transition (medium)
 * Use for: Larger panels, sheets
 */
export const fadeScaleMd = {
  enter: 'transition-all duration-300 ease-out motion-reduce:transition-opacity',
  enterFrom: 'opacity-0 scale-90 motion-reduce:scale-100',
  enterTo: 'opacity-100 scale-100',
  leave: 'transition-all duration-200 ease-in motion-reduce:transition-opacity',
  leaveFrom: 'opacity-100 scale-100',
  leaveTo: 'opacity-0 scale-90 motion-reduce:scale-100'
}

/**
 * Slide from top
 * Use for: Dropdown menus, notifications from top
 */
export const slideDown = {
  enter: 'transition-all duration-300 ease-out motion-reduce:transition-opacity',
  enterFrom: 'opacity-0 -translate-y-4 motion-reduce:translate-y-0',
  enterTo: 'opacity-100 translate-y-0',
  leave: 'transition-all duration-200 ease-in motion-reduce:transition-opacity',
  leaveFrom: 'opacity-100 translate-y-0',
  leaveTo: 'opacity-0 -translate-y-4 motion-reduce:translate-y-0'
}

/**
 * Slide from bottom
 * Use for: Toast notifications, bottom sheets
 */
export const slideUp = {
  enter: 'transition-all duration-300 ease-out motion-reduce:transition-opacity',
  enterFrom: 'opacity-0 translate-y-4 motion-reduce:translate-y-0',
  enterTo: 'opacity-100 translate-y-0',
  leave: 'transition-all duration-200 ease-in motion-reduce:transition-opacity',
  leaveFrom: 'opacity-100 translate-y-0',
  leaveTo: 'opacity-0 translate-y-4 motion-reduce:translate-y-0'
}

/**
 * Slide from right
 * Use for: Slide-over panels from right, mobile menus
 */
export const slideLeft = {
  enter: 'transition-all duration-300 ease-out motion-reduce:transition-opacity',
  enterFrom: 'opacity-0 translate-x-4 motion-reduce:translate-x-0',
  enterTo: 'opacity-100 translate-x-0',
  leave: 'transition-all duration-200 ease-in motion-reduce:transition-opacity',
  leaveFrom: 'opacity-100 translate-x-0',
  leaveTo: 'opacity-0 translate-x-4 motion-reduce:translate-x-0'
}

/**
 * Slide from left
 * Use for: Slide-over panels from left, side navigation
 */
export const slideRight = {
  enter: 'transition-all duration-300 ease-out motion-reduce:transition-opacity',
  enterFrom: 'opacity-0 -translate-x-4 motion-reduce:translate-x-0',
  enterTo: 'opacity-100 translate-x-0',
  leave: 'transition-all duration-200 ease-in motion-reduce:transition-opacity',
  leaveFrom: 'opacity-100 translate-x-0',
  leaveTo: 'opacity-0 -translate-x-4 motion-reduce:translate-x-0'
}
