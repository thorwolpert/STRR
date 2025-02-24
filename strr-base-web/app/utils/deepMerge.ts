export function deepMerge<T> (target: T, ...sources: Partial<T>[]): T {
  if (!sources.length) { return target }

  const source = sources.shift()
  if (source === undefined) { return target }

  if (isObject(target) && isObject(source)) {
    Object.keys(source).forEach((key) => {
      if (isObject(source[key])) {
        if (!target[key]) { Object.assign(target, { [key]: {} }) }
        deepMerge(target[key], source[key])
      } else {
        Object.assign(target, { [key]: source[key] })
      }
    })
  }

  return deepMerge(target, ...sources)
}

function isObject (item: any): item is Record<string, any> {
  return item && typeof item === 'object' && !Array.isArray(item)
}
