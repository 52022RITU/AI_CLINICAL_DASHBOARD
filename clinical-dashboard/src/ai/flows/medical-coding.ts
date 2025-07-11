'use server';

/**
 * @fileOverview An AI agent for medical coding assistance.
 *
 * - medicalCoding - A function that handles the medical coding process.
 * - MedicalCodingInput - The input type for the medicalCoding function.
 * - MedicalCodingOutput - The return type for the medicalCoding function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const MedicalCodingInputSchema = z.object({
  patientData: z
    .string()
    .describe('Comprehensive patient data, including demographics, vitals, and medical history.'),
  clinicalNotes: z
    .string()
    .describe('Detailed clinical notes from the doctor, including chief complaint, treatment plan, and observations.'),
});
export type MedicalCodingInput = z.infer<typeof MedicalCodingInputSchema>;

const MedicalCodingOutputSchema = z.object({
  icdCodes: z
    .array(z.string())
    .describe('An array of relevant ICD codes based on the patient data and clinical notes.'),
  codingRationale: z
    .string()
    .describe('A detailed explanation of why each ICD code was selected, referencing specific information from the patient data and clinical notes.'),
});
export type MedicalCodingOutput = z.infer<typeof MedicalCodingOutputSchema>;

export async function medicalCoding(input: MedicalCodingInput): Promise<MedicalCodingOutput> {
  return medicalCodingFlow(input);
}

const prompt = ai.definePrompt({
  name: 'medicalCodingPrompt',
  input: {schema: MedicalCodingInputSchema},
  output: {schema: MedicalCodingOutputSchema},
  prompt: `You are an AI medical coding assistant. Your task is to analyze patient data and clinical notes to suggest appropriate ICD codes.

Patient Data: {{{patientData}}}

Clinical Notes: {{{clinicalNotes}}}

Based on the information above, provide a list of relevant ICD codes and a detailed rationale for each code selection. Consider all available information to ensure accuracy and completeness.

Format the response as a JSON object with 'icdCodes' (an array of strings) and 'codingRationale' (a string explaining the reasoning behind each code).`,
});

const medicalCodingFlow = ai.defineFlow(
  {
    name: 'medicalCodingFlow',
    inputSchema: MedicalCodingInputSchema,
    outputSchema: MedicalCodingOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
