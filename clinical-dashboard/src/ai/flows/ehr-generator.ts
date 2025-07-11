'use server';

/**
 * @fileOverview An E-HR (Electronic Health Record) generation AI agent.
 *
 * - generateEhr - A function that handles the E-HR generation process.
 * - GenerateEhrInput - The input type for the generateEhr function.
 * - GenerateEhrOutput - The return type for the generateEhr function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const GenerateEhrInputSchema = z.object({
  patientDetails: z
    .string()
    .describe('Details about the patient including name, gender, age, NAT ID, nationality and insurance information.'),
  vitals: z
    .string()
    .describe('Patient vitals including temperature, blood pressure, heart rate, weight and height.'),
  chiefComplaint: z.string().describe('The patient’s primary reason for seeking medical attention.'),
  treatmentPlan: z.string().describe('The proposed course of action for managing the patient’s condition.'),
  supportingNotes: z.string().describe('Additional observations, context, or details relevant to the patient’s care.'),
  medications: z.string().describe('A list of medications prescribed to the patient.'),
  icdCodes: z.string().describe('The applicable ICD codes for the patient’s diagnosis.'),
  investigations: z.string().describe('Any diagnostic tests or procedures conducted or planned for the patient.'),
  doctorDetails: z.string().describe('Details about the doctor including name, specialty, and date.'),
});
export type GenerateEhrInput = z.infer<typeof GenerateEhrInputSchema>;

const GenerateEhrOutputSchema = z.object({
  ehrDraft: z.string().describe('A draft of the Electronic Health Record.'),
});
export type GenerateEhrOutput = z.infer<typeof GenerateEhrOutputSchema>;

export async function generateEhr(input: GenerateEhrInput): Promise<GenerateEhrOutput> {
  return generateEhrFlow(input);
}

const prompt = ai.definePrompt({
  name: 'generateEhrPrompt',
  input: {schema: GenerateEhrInputSchema},
  output: {schema: GenerateEhrOutputSchema},
  prompt: `You are an AI assistant specialized in generating draft Electronic Health Records (EHRs) for doctors.

  Based on the information provided, create a comprehensive and well-structured EHR draft.

  Patient Details: {{{patientDetails}}}
  Vitals: {{{vitals}}}
  Chief Complaint: {{{chiefComplaint}}}
  Treatment Plan: {{{treatmentPlan}}}
  Supporting Notes: {{{supportingNotes}}}
  Medications: {{{medications}}}
  ICD Codes: {{{icdCodes}}}
  Investigations: {{{investigations}}}
  Doctor Details: {{{doctorDetails}}}

  EHR Draft:
  `,
});

const generateEhrFlow = ai.defineFlow(
  {
    name: 'generateEhrFlow',
    inputSchema: GenerateEhrInputSchema,
    outputSchema: GenerateEhrOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
