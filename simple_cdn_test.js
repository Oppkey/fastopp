// Simple FontAwesome CDN injection (without integrity hash)
// Use this if you want to avoid hash validation issues

// Method 1: Simple CDN injection (no integrity hash)
const link = document.createElement('link');
link.rel = 'stylesheet';
link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css';
link.crossOrigin = 'anonymous';
document.head.appendChild(link);

console.log('✅ FontAwesome CDN injected successfully!');
