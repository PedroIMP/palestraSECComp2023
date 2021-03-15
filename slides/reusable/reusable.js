export class Reusable {
  constructor(root, options) {
    this.root = root
    this.options = {...DEFAULT_OPTIONS, ...options}
  }

  apply() {
    this.nodes = this._findNodes(this.root)
    this.reuseProviders = new Map()

    // Solve dependencies for all first
    for (let i = 0; i < this.nodes.length; i++) {
      if (!this.nodes[i].hasAttribute(this.options.reusePrefix)) {
        continue
      }
      this.reuseProviders.set(this.nodes[i], this._findReusableFor(i))
    }

    // Then apply
    for (let i = 0; i < this.nodes.length; i++) {
      if (!this.nodes[i].hasAttribute(this.options.reusePrefix)) {
        continue
      }
      this._applyReuse(i)
    }
  }

  _applyReuse(nodeIdx) {
    const template = this.nodes[nodeIdx]
    const reusable = this.reuseProviders.get(template)

    if (!reusable) {
      console.error('reusable: did not find resusable element for', template)
      return
    }

    const output = template.ownerDocument.createDocumentFragment()

    if (reusable.tagName === 'TEMPLATE') {
      output.appendChild(reusable.content.cloneNode(true))
      this._applyRules(template, output)
    } else {
      this.nodes[nodeIdx] = output.appendChild(reusable.cloneNode(true))
      this._applyRules(template, output.firstElementChild)
    }


    template.replaceWith(output)
  }


  _applyRules(template, target) {
    for (let rule of template.content.children) {
      const matches = this._getRuleMatches(target, rule)
      for (let match of matches) {
        if (rule.hasAttribute('data-replace-content')) {
          this._applyReplaceContentRule(rule, match)
        } if (rule.hasAttribute('data-append')) {
          this._applyAppendRule(rule, match)
        } else {
          this._applyReplaceContentRule(rule, match)
        }
      }
    }
  }

  _getRuleMatches(target, rule) {
    let matches = []
    if (rule.hasAttribute('data-selector')) {
      matches = target.querySelectorAll(rule.getAttribute('data-selector'))
      matches = [...matches]
    } else if (rule.hasAttribute('data-tag')) {
      const tag = rule.getAttribute('data-tag')
      const selector = `[data-reusable-tag~="${tag}"]`
      matches = target.querySelectorAll(selector)
      matches = [...matches]
    } else {
      matches = [target]
    }
    return matches
  }

  _applyReplaceContentRule(rule, match) {
    match.innerHTML = ''
    match.appendChild(rule.content.cloneNode(true))
  }

  _applyAppendRule(rule, match) {
    match.appendChild(rule.content.cloneNode(true))
  }

  _findNodes(root) {
    let selector = `[${this.options.reusablePrefix}], template[${this.options.reusePrefix}]`
    let l = [...root.querySelectorAll(selector)]

    let ambiguousTemplates = l.filter(node => {
      node.tagName === 'TEMPLATE' &&
        node.hasAttribute(this.options.reusePrefix) &&
        node.hasAttribute(this.options.reusablePrefix)
    })
    if (ambiguousTemplates.length) {
      console.warn(
        'reusable: <template> elements should not be both reusable and reuse instances. ' +
        'The following elements will only be considered reuse instances: ',
        ambiguousTemplates,
      )
    }
    ambiguousTemplates.forEach(n => {
      n.removeAttribue(this.options.reusablePrefix)
    })

    // The list l is generated by a depth-first pre-order traversal. We want it
    // to be in depth-first post-order. We will do it now.
    const stack = []
    let postOrder = []
    let i = 0
    while (i < l.length) {
      // Construct path from root to node
      let n = l[i]
      const path = []
      while (n !== root) {
        path.push(n)
        n = n.parentNode
      }
      path.reverse()

      // Find closest common ancestor in stack and path
      let pathHead = 0
      let closestStackIndex = -1
      while (pathHead < path.length && closestStackIndex + 1 < stack.length) {
        if (path[pathHead] === stack[closestStackIndex + 1]) {
          closestStackIndex++
        }
        pathHead++
      }
      // Pop elements up to (excluding) the closest ancestor and add them to
      // the reordered list.
      const popped = stack.splice(closestStackIndex + 1)
      popped.reverse()
      postOrder.push(...popped)

      stack.push(l[i])
      i++;
    }
    // Add remaining elments in the stack to the new list
    stack.reverse()
    postOrder.push(...stack)

    // querySelectorAll() does not recurse into template elements, so we need
    // to recurse ourselves.
    const r = []
    for (let node of postOrder) {
      if (node.tagName === 'TEMPLATE') {
        r.push(...this._findNodes(node.content))
      }
      r.push(node)
    }

    return r
  }

  _findReusableFor(nodeIdx) {
    const node = this.nodes[nodeIdx]
    const name = node.getAttribute(this.options.reusePrefix)
    const selector = node.getAttribute(`${this.options.reusePrefix}-selector`)
    let i = nodeIdx - 1
    while (i >= 0) {
      if (this.nodes[i].getAttribute(this.options.reusablePrefix) === name) {
        break
      }
      i--
    }

    if (i < 0) {
      return null
    }

    if (selector) {
      return this.nodes[i].querySelector(selector)
    }
    return this.nodes[i]
  }
}


const DEFAULT_OPTIONS = {
  reusablePrefix: 'data-reusable',
  reusePrefix: 'data-reuse',
}


export function applyReusable(root) {
  const reusable = new Reusable(root)
  reusable.apply()
  return reusable
}
