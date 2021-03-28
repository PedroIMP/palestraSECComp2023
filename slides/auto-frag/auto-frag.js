function processSlide(slide) {
  const autofrags = slide.querySelectorAll(':scope [data-auto-frag]')
  if (!autofrags.length) {
    return
  }

  // Generate paths
  const paths = []
  let fragIdxSeq = 0
  for (let frag of autofrags) {
    frag.dataset.autoFragIdx = fragIdxSeq++
    const path = []
    let n = frag
    while (n != slide) {
      path.push(n)
      n = n.parentNode
    }

    for (let i = 0; i < path.length; i++) {
      const idx = [...n.childNodes].indexOf(path[i])
      n = path[i]
      path[i] = idx
    }

    paths.push(path)
  }


  const numFrags = autofrags.length

  const docFragment = document.createDocumentFragment()
  // Generate the new slides
  for (let idx = 0; idx < numFrags; idx++) {
    const newSlide = slide.cloneNode(true)

    const localFrags = paths.map(path => {
      let n = newSlide
      for (let childIdx of path) {
        n = n.childNodes[childIdx]
      }
      return n
    })

    const toRemove = []
    const toSemi = []
    for (let el of localFrags) {
      const fragIdx = parseInt(el.dataset.autoFragIdx)
      const diff = idx - fragIdx
      console.log(diff)
      if (diff === 0) {
        continue
      }

      if (diff === 1) {
        toSemi.push(el)
        continue
      }

      toRemove.push(el)
    }

    for (let el of toRemove) {
      el.remove()
    }
    for (let el of toSemi) {
      el.style.opacity = .5
    }

    docFragment.appendChild(newSlide)
  }

  slide.replaceWith(docFragment)
}

export function applyAutoFrag(container) {
  const slides = container.querySelectorAll(':scope section')
  for (const slide of slides) {
    processSlide(slide)
  }
}
