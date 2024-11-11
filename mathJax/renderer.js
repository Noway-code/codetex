(function() {
    const input = document.getElementById('latex-input');
    const output = document.getElementById('rendered-output');
    let debounceTimeout;
    let lastRendered = '';
  
    const renderLaTeX = (latex) => {
      if (latex === lastRendered) return;
      lastRendered = latex;
  
      output.innerHTML = '';
      try {
        const wrappedLatex = `\\begin{align*}${latex}\\end{align*}`;
        katex.render(wrappedLatex, output, {
          throwOnError: false,
          displayMode: true,
        });
      } catch (error) {
        output.innerHTML = `<span class="error">Error: ${error.message}</span>`;
      }
    };
  
    const debounce = (func, delay) => {
      return (...args) => {
        if (debounceTimeout) clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => func.apply(this, args), delay);
      };
    };
  
    const debouncedRender = debounce(() => {
      const latex = input.value.trim();
      if (latex) {
        renderLaTeX(latex);
      } else {
        output.innerHTML = '';
        lastRendered = '';
      }
    }, 50);
  
    document.addEventListener('DOMContentLoaded', () => {
      renderLaTeX(input.value.trim());
    });
  
    input.addEventListener('input', debouncedRender);
  })();
  