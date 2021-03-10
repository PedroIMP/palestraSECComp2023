const Reusable = {}

Reusable.process = function (container) {
  const lastSeen = new Map()
  const templates = container.querySelectorAll('template[data-reusable], template[data-reuse]')

  for (let t of templates) {
    const reuse = t.dataset.reuse
    const reusable = t.dataset.reusable

    if (typeof reuse !== 'undefined') {
      if (lastSeen.has(reuse)) {
        const newNode = lastSeen.get(t.dataset.reuse).content.cloneNode(true)
        newNode.appendChild(t.content.cloneNode(true))

        const namedElements = new Map()
        for (let el of newNode.querySelectorAll('[data-reusable-name]')) {
          namedElements.set(el.dataset.reusableName, el)
        }

        const hasSavedValue = window.hasOwnProperty('$reuse')
        let savedValue
        if (hasSavedValue) {
          savedValue = window.$reuse
        }

        const parentNode = t.parentNode
        window.$reuse = (name, fn) => {
          if (!name) {
            return parentNode
          } else {
            const el = namedElements.get(name)
            if (el && fn) {
              fn(el)
            }
            return el
          }
        }
        t.replaceWith(newNode)
        if (hasSavedValue) {
          window.$reuse = savedValue
        }
      } else {
        const span = document.createElement('span')
        span.textContent = '?!NOT FOUND?!'
        t.replaceWith(span)
      }
      continue
    }

    if (typeof reusable !== 'undefined') {
      lastSeen.set(reusable, t)
    }
  }
}
