import { applyReusable } from './reusable/reusable.js'
import { applyPythonRepl } from './python-repl/python-repl.js'


const deckContainer = document.querySelector('.reveal')

applyReusable(deckContainer)
applyPythonRepl(deckContainer)

// Pre-processing of asciinema-player elements
for (let p of deckContainer.querySelectorAll('asciinema-player')) {
  if (p.hasAttribute('autoplay')) {
    if (p.pause) {
      p.pause()
      p.currentTime = 0
    }
    p.removeAttribute('autoplay')
    p.dataset.autoplay = 'true'
  } else {
    p.dataset.autoplay = 'false'
  }
}

// Initialization of the slide deck
const deck = new Reveal(deckContainer, {
  hash: true,
  plugins: [
    RevealMarkdown,
    RevealHighlight,
    RevealNotes,
    RevealAceBrython,
  ]
})

// Starting and stoping asciinema players
deck.on('ready', e => {
  for (let p of e.currentSlide.querySelectorAll('asciinema-player')) {
    if (p.dataset.autoplay === 'true') {
      p.currentTime = 0
      p.play()
    }
  }
})

deck.on('slidechanged', e => {
  // Ignore this event if e.previousSlide is undefined, which means that the
  // presentation is being loaded at a specific slide and event 'ready' will be
  // fired already. This is the current behavior of revealjs.
  // TODO: Change this depending on the outcome of
  // https://github.com/hakimel/reveal.js/issues/2915
  if (typeof e.previousSlide === 'undefined') {
    return
  }
  for (let p of e.previousSlide.querySelectorAll('asciinema-player')) {
    p.currentTime = 0
    p.pause()
  }
  for (let p of e.currentSlide.querySelectorAll('asciinema-player')) {
    if (p.dataset.autoplay === 'true') {
      p.currentTime = 0
      p.play()
    }
  }
})

deck.initialize()
