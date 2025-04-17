const fs = require('fs');
const path = require('path');

// Update imports in all JSX files
function updateImports(directory) {
  const files = fs.readdirSync(directory);
  
  files.forEach(file => {
    const filePath = path.join(directory, file);
    const stats = fs.statSync(filePath);
    
    if (stats.isDirectory()) {
      updateImports(filePath);
    } else if (file.endsWith('.jsx')) {
      let content = fs.readFileSync(filePath, 'utf8');
      
      // Update imports from components
      content = content.replace(/from ['"]\.\.\/components\/([^'"]+)['"]/g, "from '../components/$1.jsx'");
      
      // Update imports from pages
      content = content.replace(/from ['"]\.\.\/pages\/([^'"]+)['"]/g, "from '../pages/$1.jsx'");
      
      fs.writeFileSync(filePath, content);
      console.log(`Updated imports in ${filePath}`);
    }
  });
}

// Start from src directory
updateImports('./src');
