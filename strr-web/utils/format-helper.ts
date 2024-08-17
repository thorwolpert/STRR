/**
 * Formats a Date object into a long date string.
 * @param {Date} date - The date to format.
 * @returns {string} The formatted date string in 'Month Day, Year' format.
 */
export function formatLongDate (date: Date) {
  return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
}

/**
 * Formats a Date object into a time string.
 * @param {Date} date - The date to format.
 * @returns {string} The formatted time string in 'HH:MM AM/PM' format.
 */
export function formatTimeString (date: Date): string {
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}
