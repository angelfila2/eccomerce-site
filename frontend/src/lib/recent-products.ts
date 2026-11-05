const storageKey = 'pawchase-recent-products-v1'
const maximumRecentProducts = 8

export function getRecentProductIds(): string[] {
  try {
    const stored = localStorage.getItem(storageKey)
    if (!stored) return []
    const parsed: unknown = JSON.parse(stored)
    return Array.isArray(parsed) ? parsed.filter((value): value is string => typeof value === 'string') : []
  } catch {
    return []
  }
}

export function rememberProduct(productId: string): void {
  const recent = getRecentProductIds().filter((storedId) => storedId !== productId)
  localStorage.setItem(storageKey, JSON.stringify([productId, ...recent].slice(0, maximumRecentProducts)))
}
