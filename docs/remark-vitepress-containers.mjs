import { visit } from 'unist-util-visit';

/**
 * Remark plugin to convert VitePress-style containers (:::tip, :::warning, etc.)
 * to Starlight-compatible Aside components
 */
export function remarkVitepressContainers() {
  return (tree) => {
    visit(tree, (node, index, parent) => {
      // Look for ::: container syntax
      if (node.type === 'paragraph' && node.children?.[0]?.type === 'text') {
        const text = node.children[0].value;
        const containerMatch = text.match(/^:::\s*(tip|warning|note|info|details|danger|caution)/i);
        
        if (containerMatch) {
          const type = containerMatch[1].toLowerCase();
          const title = text.replace(/^:::\s*\w+\s*/, '').trim();
          
          // Find the closing :::
          let endIndex = index + 1;
          const children = [];
          
          while (endIndex < parent.children.length) {
            const nextNode = parent.children[endIndex];
            if (
              nextNode.type === 'paragraph' &&
              nextNode.children?.[0]?.type === 'text' &&
              nextNode.children[0].value.trim() === ':::'
            ) {
              break;
            }
            children.push(nextNode);
            endIndex++;
          }
          
          // Map VitePress types to Starlight types
          const typeMap = {
            tip: 'tip',
            warning: 'caution',
            danger: 'danger',
            note: 'note',
            info: 'note',
            details: 'note',
            caution: 'caution',
          };
          
          const asideType = typeMap[type] || 'note';
          
          // Create the Aside component
          const asideNode = {
            type: 'mdxJsxFlowElement',
            name: 'Aside',
            attributes: [
              {
                type: 'mdxJsxAttribute',
                name: 'type',
                value: asideType,
              },
            ],
            children: [],
            data: { _mdxExplicitJsx: true },
          };
          
          if (title) {
            asideNode.attributes.push({
              type: 'mdxJsxAttribute',
              name: 'title',
              value: title,
            });
          }
          
          asideNode.children = children;
          
          // Replace the container nodes with the Aside component
          parent.children.splice(index, endIndex - index + 1, asideNode);
        }
      }
    });
  };
}
