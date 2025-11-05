# SafePay Design System

## 🎨 Color Palette

### Primary Colors
```css
Primary:       #6366f1 (Indigo 500)
Primary Dark:  #4f46e5 (Indigo 600)
Primary Light: #818cf8 (Indigo 400)
```

### Semantic Colors
```css
Success:  #10b981 (Emerald 500)
Danger:   #ef4444 (Red 500)
Warning:  #f59e0b (Amber 500)
```

### Grayscale
```css
Gray 50:  #f8fafc
Gray 100: #f1f5f9
Gray 200: #e2e8f0
Gray 300: #cbd5e1
Gray 400: #94a3b8
Gray 500: #64748b
Gray 600: #475569
Gray 700: #334155
Gray 800: #1e293b
Gray 900: #0f172a
White:    #ffffff
```

## 📐 Spacing Scale

```
4px   → Small gaps
8px   → Base unit
12px  → Medium gaps
16px  → Section spacing
24px  → Large spacing
32px  → Extra large spacing
40px  → Page margins
```

## 🔤 Typography

### Font Family
```css
Primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
Code:    ui-monospace, 'SF Mono', Monaco, 'Cascadia Code', monospace
```

### Font Weights
```
Regular: 400
Medium:  500
Semibold: 600
Bold:    700
```

### Font Sizes
```
H1: 32px (Page titles)
H2: 28px (Section headers)
H3: 22px (Subsections)
H4: 20px (Card titles)
Body: 15px (Default text)
Small: 14px (Labels)
Tiny: 13px (Helper text)
Code: 12px (Monospace)
```

## 🎯 Shadows

```css
Shadow SM:  0 1px 2px rgba(0,0,0,0.05)
Shadow:     0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.1)
Shadow MD:  0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.1)
Shadow LG:  0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.1)
Shadow XL:  0 20px 25px rgba(0,0,0,0.1), 0 8px 10px rgba(0,0,0,0.1)
```

## 📏 Border Radius

```css
Small:  8px  (Inputs, badges)
Medium: 12px (Cards, buttons)
Large:  16px (Large containers)
Round:  999px (Pills, circular badges)
```

## ⚡ Animations

### Transitions
```css
Standard: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)
```

### Keyframes
- **fadeIn**: Opacity 0→1 with translateY
- **slideIn**: Opacity 0→1 with translateX
- **scaleIn**: Scale 0→1 with bounce
- **checkmark**: SVG stroke animation

## 🧩 Component Patterns

### Card
```
Background: White
Border: 1px solid Gray 200
Radius: 12px
Padding: 32px
Shadow: Shadow LG
Hover: Shadow XL
```

### Button (Primary)
```
Background: Linear gradient (Primary → Primary Dark)
Color: White
Padding: 12px 24px
Radius: 8px
Shadow: Shadow MD
Hover: translateY(-2px) + Shadow LG
```

### Button (Secondary)
```
Background: White
Color: Gray 700
Border: 2px solid Gray 300
Padding: 12px 24px
Radius: 8px
Hover: Background Gray 50
```

### Badge
```
Padding: 6px 12px
Radius: 16px (pill)
Font Size: 12px
Font Weight: 600
Text Transform: Uppercase
Letter Spacing: 0.5px
```

### Input Field
```
Border: 2px solid Gray 200
Radius: 8px
Padding: 12px 16px
Font Size: 15px
Focus: Border Primary + Shadow (Primary 10% opacity)
```

### Table
```
Header: Linear gradient (Primary → Primary Dark)
Header Text: White, 13px, uppercase
Row Padding: 16px
Row Hover: Background Gray 50
Border: 1px solid Gray 200 (between rows)
```

### Stat Card
```
Background: White
Border: 1px solid Gray 200
Radius: 12px
Padding: 24px
Shadow: Shadow MD
Hover: translateY(-4px) + Shadow XL
```

## 🎨 Usage Examples

### Success State
```
Background: #d1fae5
Text Color: #065f46
Icon Color: Success (#10b981)
```

### Error State
```
Background: #fee2e2
Text Color: #991b1b
Icon Color: Danger (#ef4444)
```

### Warning State
```
Background: #fef3c7
Text Color: #92400e
Icon Color: Warning (#f59e0b)
```

### Info State
```
Background: #dbeafe
Text Color: #1e40af
Icon Color: Primary (#6366f1)
```

## 📱 Responsive Breakpoints

```css
Mobile:  < 480px
Tablet:  481px - 768px
Desktop: > 768px
Max Container: 1280px
```

### Mobile Adjustments
- Navigation height: 64px (from 72px)
- Card padding: 24px (from 32px)
- Font sizes: -2px to -4px
- Tables: Horizontal scroll
- Buttons: Full width
- Grid: Single column

## 🔍 Icon System

### Size
```
Small:  14px (inline with text)
Medium: 18px (buttons)
Large:  20px (section headers)
XLarge: 24px (stat cards)
Huge:   32px (page headers)
```

### Style
- Stroke width: 2px
- Line cap: round
- Line join: round
- No fill (outline style)

## 🎯 Layout Grid

### Dashboard Stats
```
Grid: repeat(auto-fit, minmax(250px, 1fr))
Gap: 24px
```

### Form Two-Column
```
Grid: 1fr 1fr
Gap: 16px
```

### Navigation
```
Display: Flex
Justify: Space-between
Align: Center
Max Width: 1280px
Padding: 0 24px
```

## 📊 Data Visualization

### Amount Display
```
Font Size: 28px
Font Weight: 700
Color: Primary
```

### Balance Display
```
Font Size: 32px
Font Weight: 700
Color: Gray 900
```

### Stat Value
```
Font Size: 32px
Font Weight: 700
Color: Gray 900
```

### Stat Label
```
Font Size: 13px
Color: Gray 500
Text Transform: Uppercase
Letter Spacing: 0.5px
Font Weight: 600
```

## ✨ Special Effects

### Glassmorphism (Navigation)
```css
background: rgba(255, 255, 255, 0.95);
backdrop-filter: blur(10px);
```

### Gradient Text (Brand)
```css
background: linear-gradient(135deg, Primary, Primary Light);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
```

### Hover Lift
```css
transform: translateY(-2px);
box-shadow: Shadow LG;
```

## 🎨 Color Combinations

### Primary Actions
- Background: Primary gradient
- Text: White
- Icon: White

### Secondary Actions
- Background: White
- Text: Gray 700
- Border: Gray 300
- Icon: Gray 600

### Success Messages
- Background: Success light
- Text: Success dark
- Icon: Success

### Error Messages
- Background: Danger light
- Text: Danger dark
- Icon: Danger

## 📐 Spacing Patterns

### Card Spacing
```
Outer Margin: 0 auto
Inner Padding: 32px
Section Gap: 24px
Element Gap: 16px
```

### Form Spacing
```
Group Margin: 20px
Label Margin: 8px
Input Margin: 16px
```

### Table Spacing
```
Cell Padding: 16px
Row Gap: 1px (border)
Header Padding: 16px
```

## 🎯 Accessibility

### Contrast Ratios
- Body text: 4.5:1 minimum
- Large text: 3:1 minimum
- Interactive elements: 3:1 minimum

### Focus States
- Outline: 2px solid Primary
- Offset: 2px
- Visible on all interactive elements

### Touch Targets
- Minimum: 44x44px
- Buttons: 48px height minimum
- Links: Adequate padding

This design system ensures consistency across all SafePay pages and components.
