'use server';

/**
 * @fileOverview An AI agent for suggesting treatment plans based on patient data.
 *
 * - suggestTreatmentPlan - A function that suggests treatment plans.
 * - SuggestTreatmentPlanInput - The input type for the suggestTreatmentPlan function.
 * - SuggestTreatmentPlanOutput - The return type for the suggestTreatmentPlan function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const SuggestTreatmentPlanInputSchema = z.object({
  chiefComplaint: z.string().describe('The patient\'s primary reason for seeking medical attention.'),
  vitals: z.object({
    temperature: z.number().describe('The patient\'s body temperature in Celsius.'),
    bloodPressure: z.string().describe('The patient\'s blood pressure, e.g., 120/80 mmHg.'),
    heartRate: z.number().describe('The patient\'s heart rate in beats per minute.'),
    weight: z.number().describe('The patient\'s weight in kilograms.'),
    height: z.number().describe('The patient\'s height in centimeters.'),
  }).describe('The patient\'s vital signs.'),
  notes: z.string().describe('Additional clinical notes about the patient.'),
  medications: z.string().describe('Current medications the patient is taking.'),
  icdCodes: z.string().describe('ICD codes relevant to the patient\'s condition.'),
  investigations: z.string().describe('Results of any investigations, such as lab tests or imaging.'),
});
export type SuggestTreatmentPlanInput = z.infer<typeof SuggestTreatmentPlanInputSchema>;

const SuggestTreatmentPlanOutputSchema = z.object({
  treatmentPlanSuggestions: z.array(z.string()).describe('A list of suggested treatment plans, with clear explanations.'),
  supportingEvidence: z.string().describe('Evidence from medical literature or databases that supports the suggested treatment plans.'),
  risksAndBenefits: z.string().describe('A discussion of the potential risks and benefits of each suggested treatment plan.'),
});
export type SuggestTreatmentPlanOutput = z.infer<typeof SuggestTreatmentPlanOutputSchema>;

export async function suggestTreatmentPlan(input: SuggestTreatmentPlanInput): Promise<SuggestTreatmentPlanOutput> {
  return suggestTreatmentPlanFlow(input);
}

const prompt = ai.definePrompt({
  name: 'suggestTreatmentPlanPrompt',
  input: {schema: SuggestTreatmentPlanInputSchema},
  output: {schema: SuggestTreatmentPlanOutputSchema},
  prompt: `You are an AI assistant that suggests treatment plans for doctors based on patient information.

  Given the following patient data, suggest possible treatment plans:

  Chief Complaint: {{{chiefComplaint}}}
  Vitals: Temperature: {{{vitals.temperature}}} °C, Blood Pressure: {{{vitals.bloodPressure}}}, Heart Rate: {{{vitals.heartRate}}} bpm, Weight: {{{vitals.weight}}} kg, Height: {{{vitals.height}}} cm
  Notes: {{{notes}}}
  Medications: {{{medications}}}
  ICD Codes: {{{icdCodes}}}
  Investigations: {{{investigations}}}

  Provide a list of treatment plan suggestions, supporting evidence from medical literature, and a discussion of the risks and benefits of each plan.
  Output the treatment plans as a JSON array of strings, supporting evidence as a string, and risks and benefits as a string.
  Make sure to follow the SuggestTreatmentPlanOutputSchema. The schema descriptions are:
  ${JSON.stringify(SuggestTreatmentPlanOutputSchema.shape, null, 2)}
  `,
});

const suggestTreatmentPlanFlow = ai.defineFlow(
  {
    name: 'suggestTreatmentPlanFlow',
    inputSchema: SuggestTreatmentPlanInputSchema,
    outputSchema: SuggestTreatmentPlanOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
