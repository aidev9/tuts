### UX Style Guide for React Web Application

---

#### **1. Typography**

A consistent and clear typography system enhances readability and maintains a cohesive brand identity.

- **Font Family:**

  - Primary: `'Roboto', sans-serif;`
  - Secondary: `'Open Sans', sans-serif;`

- **Font Weights:**

  - Light: 300
  - Regular: 400
  - Medium: 500
  - Bold: 700

- **Font Sizes:**

  - Heading 1 (H1): 48px / 3rem
  - Heading 2 (H2): 40px / 2.5rem
  - Heading 3 (H3): 32px / 2rem
  - Heading 4 (H4): 24px / 1.5rem
  - Paragraph: 16px / 1rem
  - Small Text: 14px / 0.875rem
  - Caption: 12px / 0.75rem

- **Line Heights:**

  - Headings: 1.3
  - Body Text: 1.6

- **Letter Spacing:**
  - Headings: Normal
  - Body Text: 0.5px

---

#### **2. Color Palette**

The color palette helps create a visually consistent and brand-aware experience. Make sure to adhere to WCAG contrast guidelines for accessibility.

- **Primary Colors:**

  - Primary Color: `#1A73E8` (Blue)
  - Primary Dark: `#174EA6` (Darker Blue)
  - Primary Light: `#E8F0FE` (Lighter Blue)

- **Secondary Colors:**

  - Secondary Color: `#F9A825` (Yellow)
  - Secondary Dark: `#C17900` (Darker Yellow)
  - Secondary Light: `#FFECB3` (Lighter Yellow)

- **Neutral Colors:**

  - White: `#FFFFFF`
  - Light Gray: `#F5F5F5`
  - Gray: `#9E9E9E`
  - Dark Gray: `#616161`
  - Black: `#212121`

- **Accent Colors:**
  - Error: `#D32F2F` (Red)
  - Success: `#388E3C` (Green)
  - Info: `#0288D1` (Cyan)
  - Warning: `#FFA000` (Amber)

---

#### **3. Button Styles**

Buttons should follow the consistent sizing, colors, and typography patterns to maintain usability and branding.

- **Primary Button:**

  - Background Color: `#1A73E8`
  - Text Color: `#FFFFFF`
  - Hover Background: `#174EA6`
  - Padding: 12px 24px
  - Border Radius: 4px

- **Secondary Button:**

  - Background Color: `#F9A825`
  - Text Color: `#212121`
  - Hover Background: `#C17900`
  - Padding: 12px 24px
  - Border Radius: 4px

- **Disabled Button:**
  - Background Color: `#E0E0E0`
  - Text Color: `#9E9E9E`
  - Cursor: `not-allowed`

---

#### **4. Spacing and Grid System**

The spacing system ensures consistency in layout and component padding/margins. A 4px grid system provides flexibility.

- **Base Spacing Unit:** 4px

  - Small Margin/Padding: 8px
  - Medium Margin/Padding: 16px
  - Large Margin/Padding: 32px

- **Container Widths:**
  - Small (mobile): 360px - 480px
  - Medium (tablet): 768px - 1024px
  - Large (desktop): 1200px+

---

#### **5. Breakpoints (Responsive Design)**

Design should adapt to various device sizes using media queries.

- **Breakpoints:**
  - Mobile: `@media (max-width: 480px)`
  - Tablet: `@media (max-width: 768px)`
  - Desktop: `@media (max-width: 1024px)`
  - Large Screen: `@media (max-width: 1200px)`

---

#### **6. Form Elements**

- **Input Fields:**

  - Border: 1px solid `#9E9E9E`
  - Focus Border: 2px solid `#1A73E8`
  - Placeholder Color: `#BDBDBD`
  - Text Color: `#212121`
  - Padding: 12px 16px
  - Border Radius: 4px

- **Error States:**

  - Border Color: `#D32F2F`
  - Text Color: `#D32F2F`

- **Label:**
  - Font Size: 14px
  - Font Weight: 500
  - Color: `#616161`

---

#### **7. Iconography**

- Use consistent iconography across the application for actions and status indicators.
- Recommended Library: [Material-UI Icons](https://material-ui.com/components/icons/)

---

#### **8. Shadows & Elevation**

- **Card Shadow:**

  - Default: `0px 4px 6px rgba(0, 0, 0, 0.1)`
  - Hover: `0px 6px 8px rgba(0, 0, 0, 0.15)`

- **Elevation Levels:**
  - Small: `0px 2px 4px rgba(0, 0, 0, 0.05)`
  - Medium: `0px 4px 6px rgba(0, 0, 0, 0.1)`
  - Large: `0px 8px 12px rgba(0, 0, 0, 0.15)`

---

#### **9. Accessibility**

- **Contrast Ratio:**

  - Text over background: Minimum 4.5:1
  - Large text: Minimum 3:1

- **Keyboard Navigation:**

  - Ensure all focusable elements (buttons, inputs) have clear focus styles.
  - Use `outline` or `box-shadow` for focus indicators: `outline: 2px solid #1A73E8;`

- **ARIA Labels:**
  - Use appropriate ARIA roles and labels for screen reader accessibility.

---

#### **10. Animations**

- **Transition Duration:**

  - Fast: `150ms`
  - Normal: `300ms`
  - Slow: `500ms`

- **Easing:**
  - Default: `ease-in-out`
  - Hover Effects: `ease-out`

---

This UX style guide ensures a unified brand experience across your React web application, helping developers maintain consistency while promoting accessibility, usability, and responsiveness.
