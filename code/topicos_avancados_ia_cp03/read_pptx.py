import zipfile
import xml.etree.ElementTree as ET

pptx_path = r'C:\Users\ccunh\Downloads\AI4Good_Distopia_Utopia (3).pptx'

try:
    z = zipfile.ZipFile(pptx_path)
    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
    }
    
    slides = [f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
    # Sort slides correctly: slide1.xml, slide2.xml...
    slides.sort(key=lambda x: int(x.replace('ppt/slides/slide','').replace('.xml','')))
    
    for i, slide in enumerate(slides):
        root = ET.fromstring(z.read(slide))
        texts = [node.text for node in root.findall('.//a:t', ns) if node.text]
        print(f"\n--- Slide {i+1} ---")
        print(" ".join(texts))
        
except Exception as e:
    print(f"Error reading pptx: {e}")
