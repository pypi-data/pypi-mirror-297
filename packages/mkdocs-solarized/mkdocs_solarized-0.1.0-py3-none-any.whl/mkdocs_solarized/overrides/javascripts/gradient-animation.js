document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('button, .md-button');

    buttons.forEach(button => {
        button.addEventListener('mousemove', function (e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const xPercent = (x / this.offsetWidth) * 100;
            const yPercent = (y / this.offsetHeight) * 100;

            const gradientStart = getComputedStyle(this).getPropertyValue('--button-gradient-start');
            const gradientEnd = getComputedStyle(this).getPropertyValue('--button-gradient-end');

            // Apply a radial gradient centered at the cursor's position
            this.style.backgroundImage = `radial-gradient(circle at ${xPercent}% ${yPercent}%, ${gradientStart} 0%, ${gradientEnd} 100%)`;
        });

        button.addEventListener('mouseleave', function () {
            // Smooth transition back to the default gradient without the red flash
            // Optionally, you might want to add a slight delay before resetting the gradient
            setTimeout(() => {
                this.style.backgroundImage = 'none';  // Ensure this is set to the original background state
            }, 50);  // Delay can be adjusted based on how the transition looks
        });
    });
});
