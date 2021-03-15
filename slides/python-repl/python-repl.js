const ENTRY_TEMPLATE = document.createElement('template')
ENTRY_TEMPLATE.innerHTML =
  `<div class="python-repl-entry">
    <div class="python-repl-code"></div>
    <div class="python-repl-output"></div>
  </div>`


function getContent(container) {
  if (!container.textContent && container.childNodes.length === 1 &&
      container.childNodes[0].nodeType === Node.COMMENT_NODE) {
    return container.childNodes[0].textContent
  } else {
    return container.textContent
  }
}


function getLines(container) {
  const content = getContent(container)
  const allLines = content.split(/\r?\n/g)
  let start = 0
  while (start < allLines.length && /^\s*$/.test(allLines[start])) {
    start++
  }

  let end = allLines.length
  while (end > 0 && /^\s*$/.test(allLines[end - 1])) {
    end--
  }

  let padding
  let lines = allLines.slice(start, end).map((line, i) => {
    if (i === 0) {
      padding = line.match(/^\s*/)[0]
    } else if (!line.startsWith(padding)){
      const msg = `mismatched padding on line ${start + i + 1}`
      console.error(msg, container)
      throw new Error(msg)
    }
    return line.slice(padding.length)
  })

  return [lines, start, end]
}


function parseLines(lines, lineNumberOffset) {
  let lineIdx = 0

  function error(msg) {
    msg = `line ${getLineNumber()}: ${msg}`
    throw new Error(msg)
  }

  function getLineNumber() {
    if (lineIdx < lines.length) {
      return (lineIdx + lineNumberOffset + 1)
    } else {
      return 'EOF'
    }
  }

  function parseDirectives() {
    let json = ''
    const lineNumber = getLineNumber()
    while (lineIdx < lines.length && lines[lineIdx].startsWith('### ')) {
      json += lines[lineIdx].slice(4)
      lineIdx++;
    }
    json = json.trim()

    if (json) {
      try {
        const directives = JSON.parse(json)
      } catch (e) {
        error(`error parsing directives JSON: ${e}`)
      }
      return {directives, directivesLineNumber: lineNumber}
    }
    return null
  }

  function parseCode() {
    if (lineIdx >= lines.length || !lines[lineIdx].startsWith('>>> ')) {
      error('expected prefix ">>> "')
    }
    let lineNumber = getLineNumber()
    const codeLines = [lines[lineIdx++].slice(4)]
    while (lineIdx < lines.length && lines[lineIdx].startsWith('... ')) {
      codeLines.push(lines[lineIdx++].slice(4))
    }
    return {lineNumber, lines: codeLines}
  }

  function parseOutput() {
    const lineNumber = null
    let outputLines = []
    while (lineIdx < lines.length) {
      if (lines[lineIdx].startsWith('### ') || lines[lineIdx].startsWith('>>> ')) {
        break
      }
      outputLines.push(lines[lineIdx++])
    }
    outputLines = outputLines.map(s => s.startsWith('@') ? s.slice(1) : s)
    return {
      lineNumber,
      lines: outputLines,
    }
  }

  const r = []
  while (lineIdx < lines.length) {
    const entry = {
      code: {
        lines: [],
        lineNumber: null,
        directives: null,
        directivesLineNumber: null,
      },
      output: {
        lines: [],
        lineNumber: null,
        directives: null,
        directivesLineNumber: null,
      }
    }

    Object.assign(entry.code, parseDirectives())
    Object.assign(entry.code, parseCode())
    Object.assign(entry.output, parseDirectives())
    Object.assign(entry.output, parseOutput())

    r.push(entry)
  }
  return r
}


function buildEntryElements(container, entry, entryIdx) {
  const entryFrag = ENTRY_TEMPLATE.content.cloneNode(true)
  const entryEl = entryFrag.firstElementChild

  entryEl.dataset.entryIndex = entryIdx

  const codeEl = entryEl.querySelector('.python-repl-code')
  for (const line of entry.code.lines) {
    const lineEl = codeEl.appendChild(document.createElement('div'))
    lineEl.className = 'python-repl-code-line'
    lineEl.textContent = line
  }

  const outputEl = entryEl.querySelector('.python-repl-output')
  for (const line of entry.output.lines) {
    const lineEl = outputEl.appendChild(document.createElement('div'))
    lineEl.className = 'python-repl-output-line'
    lineEl.textContent = line
  }

  container.appendChild(entryFrag)
}


function init(container) {
  const [lines, start, end] = getLines(container)

  let entries
  try {
    entries = parseLines(lines, start)
  } catch (e) {
    console.error(`error parsing Python REPL lines: ${e}`, container)
    throw new Error(`error parsing Python REPL lines: ${e}`)
  }

  container.innerHTML = ''
  entries.forEach((entry, entryIdx) => {
    buildEntryElements(container, entry, entryIdx)
  })
}


export function applyPythonRepl(root) {
  for (let container of root.querySelectorAll('.python-repl')) {
    init(container)
  }
}
