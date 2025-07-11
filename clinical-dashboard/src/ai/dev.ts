import { config } from 'dotenv';
config();

import '@/ai/flows/suggest-treatment-plan.ts';
import '@/ai/flows/medical-coding.ts';
import '@/ai/flows/ai-advisory.ts';
import '@/ai/flows/ehr-generator.ts';