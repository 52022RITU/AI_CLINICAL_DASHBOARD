# MediDash AI - AI-Powered Clinical Dashboard

MediDash AI is a modern, responsive web application built with Next.js that serves as an AI-powered clinical dashboard for healthcare professionals. It provides tools to manage patient data and leverages generative AI to assist with clinical decision-making, medical coding, and administrative tasks.

## ✨ Features

- **Intuitive Dashboard:** A central hub for viewing and managing patient information.
- **Dynamic Patient Data:** View and manage patient details, vitals, and clinical notes.
- **AI-Powered Actions:**
    - **Medical Coding:** Automatically suggest ICD codes based on clinical notes.
    - **AI Advisory:** Get AI-generated advice on patient care and treatment plans.
    - **Treatment Suggestions:** Receive evidence-based treatment plan suggestions.
    - **E-HR Generation:** Automatically generate draft Electronic Health Records.
- **Responsive Design:** A seamless experience across desktop and mobile devices.
- **Modern UI:** Built with ShadCN UI and Tailwind CSS for a clean and professional look.

## 🚀 Tech Stack

- **Framework:** [Next.js](https://nextjs.org/) (App Router)
- **Language:** [TypeScript](https://www.typescriptlang.org/)
- **UI:** [React](https://react.dev/)
- **Styling:** [Tailwind CSS](https://tailwindcss.com/)
- **Component Library:** [ShadCN UI](https://ui.shadcn.com/)
- **AI Integration:** [Genkit](https://firebase.google.com/docs/genkit)
- **Form Management:** [React Hook Form](https://react-hook-form.com/) & [Zod](https://zod.dev/) for validation

## 📦 Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/en) 
- [npm](https://www.npmjs.com/) or [yarn](https://yarnpkg.com/)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root of the project and add any necessary environment variables (e.g., API keys for Google AI).

    ```
    # .env
    GOOGLE_API_KEY=your_google_ai_api_key
    ```

### Running the Application

1.  **Start the development server:**
    ```bash
    npm run dev
    ```
    The application will be available at `http://localhost:9002`.

2.  **Start the Genkit development server (for AI features):**
    In a separate terminal, run:
    ```bash
    npm run genkit:dev
    ```
    This starts the Genkit developer UI, which allows you to inspect and test your AI flows.

## 📁 Project Structure

```
.
├── src/
│   ├── app/                # Next.js App Router pages and layouts
│   ├── ai/                 # Genkit AI integration
│   │   ├── flows/          # AI flows (e.g., medical coding, suggestions)
│   │   └── genkit.ts       # Genkit configuration
│   ├── components/         # Reusable React components
│   │   ├── ui/             # ShadCN UI components
│   │   └── ...
│   ├── hooks/              # Custom React hooks
│   └── lib/                # Utility functions
├── public/                 # Static assets
└── ...                     # Configuration files
```


