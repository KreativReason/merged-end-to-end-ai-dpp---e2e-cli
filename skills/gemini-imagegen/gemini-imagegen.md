# Gemini Image Generation Skill

## Purpose

Generate images using Google's Gemini API for UI mockups, placeholder content, and visual assets.

## Capabilities

- Generate placeholder images
- Create UI mockups
- Generate icons and illustrations
- Create avatar/profile images
- Generate product images

## API Integration

```javascript
// Gemini API configuration
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-pro-vision" });
```

## Usage

### Generate Image

```javascript
async function generateImage(prompt, options = {}) {
  const {
    width = 512,
    height = 512,
    style = 'realistic',
    format = 'png'
  } = options;

  const result = await model.generateContent({
    prompt: `Generate an image: ${prompt}`,
    generationConfig: {
      width,
      height,
      style
    }
  });

  return result.image;
}
```

### Common Use Cases

#### Placeholder Images
```javascript
await generateImage("Professional headshot placeholder, neutral background", {
  width: 200,
  height: 200,
  style: 'professional'
});
```

#### UI Mockups
```javascript
await generateImage("Dashboard UI mockup with charts and metrics", {
  width: 1200,
  height: 800,
  style: 'clean-ui'
});
```

#### Product Images
```javascript
await generateImage("Generic product box on white background", {
  width: 400,
  height: 400,
  style: 'product-photography'
});
```

## Style Presets

| Style | Description |
|-------|-------------|
| `realistic` | Photo-realistic images |
| `illustration` | Hand-drawn style |
| `clean-ui` | Minimal UI mockups |
| `product-photography` | Product shots |
| `abstract` | Abstract patterns |
| `icon` | Simple icons |

## Output Schema

```json
{
  "status": "success",
  "image": {
    "url": "generated/image-123.png",
    "width": 512,
    "height": 512,
    "format": "png",
    "size_bytes": 45678
  },
  "prompt_used": "Dashboard UI mockup...",
  "generation_time_ms": 2340
}
```

## Integration

Used by:
- `design-iterator` for generating visual assets
- `/kreativreason:work` for placeholder content
- Documentation generation for illustrations

## Rate Limits

- 60 requests per minute
- 1000 requests per day
- Images cached for 24 hours

## Environment Variables

```bash
GEMINI_API_KEY=your-api-key
GEMINI_IMAGE_CACHE_DIR=.cache/images
```
