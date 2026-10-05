# Project guidance

Read `CONTEXT.md` before helping with this project. It records the goals, hardware,
learning progress, and next milestone. Treat it as a dated snapshot; inspect the
current code before making claims about what is implemented or working.

## Learning preferences

- This is an embedded C++ / STM32 / FreeRTOS learning project and interview portfolio.
- Default to teaching: short explanations, documentation pointers, and one small
  next step. Let the user write the implementation.
- Do not edit firmware or flash hardware unless explicitly requested. Asking for
  a review, explanation, nudge, or example in chat is not a request to change code.
- Explain why things work. Distinguish language requirements from conventions,
  especially declarations, definitions, headers, linkage, and file organization.
- The user wants to understand and develop the VL53L1X driver. Use vendor code as
  a reference rather than silently substituting a finished implementation.
- Focus on reading a sensor measurement and printing it over UART before adding
  scanner motion, advanced RTOS architecture, or mapping.
- Keep the README concise. Keep detailed learning context in `CONTEXT.md`, and
  distinguish configured peripherals from hardware-tested functionality.
