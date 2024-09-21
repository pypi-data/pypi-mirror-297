document.addEventListener("DOMContentLoaded", function() {
    const header = document.querySelector('h1:first-of-type');
    if (!header) return; // If no h1 is found, exit the function
  
    const text = header.textContent.replace(/¶/g, '').trim();
    header.innerHTML = ""; // Clear the header to start fresh
  
    // Create a span for the prefix and append it to the header
    const prefixSpan = document.createElement('span');
    prefixSpan.textContent = '~:/ ';
    prefixSpan.className = 'prefix';
    prefixSpan.style.opacity = 0; // Start prefix as invisible
    header.appendChild(prefixSpan);
  
    // Create spans for each character in the text
    text.split('').forEach(char => {
      const charSpan = document.createElement('span');
      charSpan.textContent = char;
      charSpan.className = 'text-char';
      charSpan.style.opacity = 0; // Start characters as invisible
      header.appendChild(charSpan);
    });
  
    const cursorSpan = document.createElement('span');
    cursorSpan.textContent = '_';
    cursorSpan.className = 'blinking-underscore';
    header.appendChild(cursorSpan); // Append the underscore at the end initially
  
    let index = 0;
    function typeWriter() {
      const elements = header.querySelectorAll('.prefix, .text-char');
      if (index < elements.length) {
        elements[index].style.opacity = 1; // Make the character visible
        elements[index].style.backgroundColor = "#073642"; // Solarized Base02, darker background
        cursorSpan.remove(); // Remove the cursor from its current position
        if (index < elements.length - 1) {
          elements[index + 1].before(cursorSpan); // Move the cursor to the next position
        } else {
          elements[index].after(cursorSpan); // Move the cursor to the end after the last character
        }
        index++;
        setTimeout(typeWriter, 150); // Control the speed of the typewriter effect
      }
    }
  
    typeWriter();
  });
  