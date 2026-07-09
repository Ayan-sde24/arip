export interface MockAnalysis {
  id: string;
  candidateName: string;
  role: string;
  date: string;
  scores: {
    overall: number;
    ats: number;
    recruiter: number;
    semantic: number;
    optimization: number;
  };
  matchedSkills: string[];
  missingSkills: string[];
  status: "completed" | "failed";
}

export const MOCK_ANALYSES: MockAnalysis[] = [
  {
    id: "an-9082",
    candidateName: "Alex Mercer",
    role: "Senior Full Stack Engineer",
    date: "2026-07-08",
    scores: { overall: 85, ats: 88, recruiter: 80, semantic: 84, optimization: 88 },
    matchedSkills: ["React", "TypeScript", "Node.js", "PostgreSQL", "REST APIs", "Docker", "Git"],
    missingSkills: ["Kubernetes", "AWS ECS", "Terraform", "Redis"],
    status: "completed"
  },
  {
    id: "an-1294",
    candidateName: "Sarah Connor",
    role: "Lead DevOps Engineer",
    date: "2026-07-05",
    scores: { overall: 91, ats: 94, recruiter: 88, semantic: 90, optimization: 92 },
    matchedSkills: ["AWS", "Kubernetes", "Terraform", "Docker", "Ansible", "CI/CD", "Python", "Bash"],
    missingSkills: ["Prometheus", "Grafana", "ArgoCD"],
    status: "completed"
  },
  {
    id: "an-3829",
    candidateName: "Bruce Banner",
    role: "Data Scientist & ML Engineer",
    date: "2026-07-02",
    scores: { overall: 74, ats: 71, recruiter: 78, semantic: 72, optimization: 75 },
    matchedSkills: ["Python", "TensorFlow", "Pandas", "NumPy", "SQL", "Git"],
    missingSkills: ["PyTorch", "Kubeflow", "Mlflow", "Spark"],
    status: "completed"
  },
  {
    id: "an-8302",
    candidateName: "Tony Stark",
    role: "Principal Embedded Systems Engineer",
    date: "2026-06-29",
    scores: { overall: 96, ats: 98, recruiter: 94, semantic: 96, optimization: 98 },
    matchedSkills: ["C++", "C", "RTOS", "Microcontrollers", "Embedded Linux", "Assembly", "SPI/I2C"],
    missingSkills: ["Rust", "CAN bus"],
    status: "completed"
  }
];

export const MOCK_RESUME_TEXT = `ALEX MERCER
Senior Full Stack Engineer
alex.mercer@email.com | +1 (555) 019-2831 | github.com/alexmercer

SUMMARY
Product-focused Software Engineer with 6+ years of experience designing and deploying scalable web applications. Expert in React, Node.js, and relational database systems. Proven track record of improving system latency and leading agile development squads.

EXPERIENCE
Senior Software Engineer | CloudTech Solutions (2023 - Present)
* Led rewrite of flagship product from legacy codebase to modern React 18/TypeScript, improving first-contentful paint by 35%.
* Built high-throughput API endpoints utilizing Express and PostgreSQL, handling over 10M daily requests.
* Spearheaded transition to a containerized Docker architecture, reducing developer onboarding times by half.
* Mentored 4 junior developers and established code review guidelines to ensure consistency.

Software Engineer | WebDev Innovations (2020 - 2023)
* Developed and shipped custom visual dashboards for enterprise clients, increasing customer retention by 12%.
* Optimized database queries in PostgreSQL, reducing query execution times by 40% on peak loads.
* Implemented CI/CD pipelines via GitHub Actions, speeding up release cycles from bi-weekly to daily deployments.

SKILLS
* Frontend: React, Redux, HTML5, CSS3, TailwindCSS, TypeScript
* Backend: Node.js, Express, REST APIs, GraphQL, PostgreSQL
* DevOps & Tools: Docker, Git, CI/CD (GitHub Actions), Linux`;

export const MOCK_JD_TEXT = `Position: Senior Full Stack Engineer (AI Platform)
Location: Remote / Hybrid

About the Role:
We are seeking a Senior Full Stack Engineer to scale our core AI analysis workspace. You will work on expanding pipeline processing engines, building rich visual dashboards, and implementing high-performance API structures.

Required Qualifications:
- 5+ years of software engineering experience.
- Deep expertise in modern frontend frameworks (React, TypeScript).
- Solid experience writing production Node.js APIs and optimizing relational databases (PostgreSQL).
- Hands-on experience with containerization (Docker) and cloud deployments (AWS, Kubernetes, Terraform).
- Strong communication skills and leadership capability.

Preferred:
- Familiarity with caching databases (Redis) and cloud monitoring systems.`;

export const MOCK_OPTIMIZER_CHANGES = [
  {
    id: "opt-1",
    section: "Summary",
    original: "Product-focused Software Engineer with 6+ years of experience designing and deploying scalable web applications.",
    suggested: "Product-focused Senior Full Stack Engineer with 6+ years of experience designing and deploying scalable web applications with Kubernetes and AWS ECS cloud deployments.",
    explanation: "Injected target keywords 'Senior Full Stack Engineer', 'Kubernetes', and 'AWS ECS' to align summary directly with JD requirements.",
    accepted: false,
    rejected: false,
  },
  {
    id: "opt-2",
    section: "Experience",
    original: "Led rewrite of flagship product from legacy codebase to modern React 18/TypeScript, improving first-contentful paint by 35%.",
    suggested: "Led engineering rewrite of flagship React/TypeScript SaaS workspace, reducing FCP by 35% and increasing query speeds via Redis caching.",
    explanation: "Introduced 'SaaS workspace' and 'Redis' caching references to target preferred job description skill additions.",
    accepted: false,
    rejected: false,
  },
  {
    id: "opt-3",
    section: "Experience",
    original: "Built high-throughput API endpoints utilizing Express and PostgreSQL, handling over 10M daily requests.",
    suggested: "Engineered scalable REST APIs in Node.js/PostgreSQL containerized on Docker, handling 10M+ daily transactions under AWS ECS.",
    explanation: "Enhanced metric description with keywords 'REST APIs', 'Node.js', 'Docker', and 'AWS ECS' for better keyword scoring.",
    accepted: false,
    rejected: false,
  },
  {
    id: "opt-4",
    section: "Skills",
    original: "* Frontend: React, Redux, HTML5, CSS3, TailwindCSS, TypeScript\n* Backend: Node.js, Express, REST APIs, GraphQL, PostgreSQL",
    suggested: "* Frontend: React, Redux, HTML5, CSS3, TailwindCSS, TypeScript\n* Backend: Node.js, Express, REST APIs, GraphQL, PostgreSQL, Redis\n* Cloud & DevOps: Docker, Kubernetes, Terraform, AWS ECS, CI/CD, Git",
    explanation: "Added AWS ECS, Kubernetes, Redis, and Terraform directly into the core skills breakdown to avoid filter exclusions.",
    accepted: false,
    rejected: false,
  }
];

export const MOCK_RADAR_DATA = [
  { subject: "React & TypeScript", score: 92 },
  { subject: "Node.js & Postgres", score: 85 },
  { subject: "DevOps & Docker", score: 78 },
  { subject: "Cloud Infrastructure", score: 55 },
  { subject: "System Design", score: 70 },
  { subject: "Leadership / Mentor", score: 80 },
];
