"use client";

import { useState } from 'react';
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

import { PatientHeader } from './patient-header';
import { VitalsBar } from './vitals-bar';
import { ClinicalDataForm, clinicalDataSchema } from './clinical-data-form';
import { AiActions } from './ai-actions';
import { AiModal } from './ai-modal';
import { useToast } from '@/hooks/use-toast';

import { medicalCoding } from '@/ai/flows/medical-coding';
import { aiAdvisory } from '@/ai/flows/ai-advisory';
import { suggestTreatmentPlan } from '@/ai/flows/suggest-treatment-plan';
import { generateEhr } from '@/ai/flows/ehr-generator';

export type AiActionType = 'coding' | 'advisory' | 'suggestions' | 'claims' | 'ehr';

export default function Dashboard() {
    const [modalState, setModalState] = useState<{ open: boolean, title: string, content: string, isLoading: boolean }>({
        open: false,
        title: '',
        content: '',
        isLoading: false,
    });

    const { toast } = useToast();

    const form = useForm<z.infer<typeof clinicalDataSchema>>({
        resolver: zodResolver(clinicalDataSchema),
        defaultValues: {
            chiefComplaint: "Patient reports experiencing intermittent, sharp chest pains over the past 48 hours, accompanied by shortness of breath upon mild exertion. No fever or other symptoms reported.",
            treatmentPlan: "Administer sublingual nitroglycerin as needed for pain. Schedule for an urgent ECG and cardiac enzyme test. Follow up with a cardiology consultation.",
            supportingNotes: "Patient has a family history of heart disease. Smoker, approximately 10 cigarettes a day. Appears anxious.",
            medications: "Lisinopril 10mg daily",
            icdCodes: "R07.9, I10",
            investigations: "Pending ECG and blood work.",
        },
    });

    const handleAiAction = async (action: AiActionType) => {
        const isValid = await form.trigger();
        if (!isValid) {
            toast({
                variant: "destructive",
                title: "Validation Error",
                description: "Please fill in all mandatory fields before using AI actions.",
            });
            return;
        }

        const formData = form.getValues();
        const patientData = `Name: John Doe, Gender: Male, Age: 45, NAT ID: 123456789, Nationality: American, Insurance: Blue Cross`;
        const vitals = `Temp: 37°C, BP: 120/80 mmHg, HR: 72 bpm, Weight: 85 kg, Height: 180 cm`;
        const doctorDetails = `Dr. Smith, Cardiology, ${new Date().toLocaleDateString()}`;

        let modalTitle = '';
        let promise: Promise<any>;

        setModalState({ open: true, title: 'Thinking...', content: '', isLoading: true });

        switch (action) {
            case 'coding':
                modalTitle = 'AI Medical Coding';
                promise = medicalCoding({
                    patientData,
                    clinicalNotes: `Chief Complaint: ${formData.chiefComplaint}\nTreatment Plan: ${formData.treatmentPlan}\nNotes: ${formData.supportingNotes}`,
                });
                break;
            case 'advisory':
                modalTitle = 'AI Advisory';
                promise = aiAdvisory({
                    patientDetails: patientData,
                    vitals,
                    chiefComplaint: formData.chiefComplaint,
                    treatmentPlan: formData.treatmentPlan || 'Not specified',
                    supportingNotes: formData.supportingNotes || 'None',
                    medications: formData.medications || 'None',
                    icdCodes: formData.icdCodes || 'None',
                    investigations: formData.investigations || 'None',
                });
                break;
            case 'suggestions':
                modalTitle = 'Treatment Suggestions';
                promise = suggestTreatmentPlan({
                    chiefComplaint: formData.chiefComplaint,
                    vitals: { temperature: 37, bloodPressure: '120/80', heartRate: 72, weight: 85, height: 180 },
                    notes: formData.supportingNotes || 'None',
                    medications: formData.medications || 'None',
                    icdCodes: formData.icdCodes || 'None',
                    investigations: formData.investigations || 'None',
                });
                break;
            case 'claims':
                modalTitle = 'Claims Database';
                promise = new Promise(resolve => setTimeout(() => resolve({ "AI Analysis": "Based on the provided ICD codes, similar claims have a 95% approval rate.\n\nPotential Flags: None noted.\n\nRecommendations: Ensure all documentation for the ECG and cardiac enzyme tests are attached to the claim to expedite processing." }), 1000));
                break;
            case 'ehr':
                modalTitle = 'Generate E-HR';
                promise = generateEhr({
                    patientDetails: patientData,
                    vitals,
                    chiefComplaint: formData.chiefComplaint,
                    treatmentPlan: formData.treatmentPlan || 'Not specified',
                    supportingNotes: formData.supportingNotes || 'None',
                    medications: formData.medications || 'None',
                    icdCodes: formData.icdCodes || 'None',
                    investigations: formData.investigations || 'None',
                    doctorDetails,
                });
                break;
            default:
                setModalState({ open: false, title: '', content: '', isLoading: false });
                return;
        }

        setModalState(s => ({ ...s, title: modalTitle }));

        try {
            const result = await promise;
            const formattedResult = Object.entries(result)
                .map(([key, value]) => `\n--- ${key.replace(/([A-Z])/g, ' $1').trim().toUpperCase()} ---\n\n${Array.isArray(value) ? value.join('\n- ') : value}`)
                .join('\n');
            setModalState(s => ({ ...s, content: formattedResult, isLoading: false }));
        } catch (error) {
            console.error(error);
            setModalState({ open: false, title: '', content: '', isLoading: false });
            toast({
                variant: "destructive",
                title: "AI Action Failed",
                description: "There was an error processing your request.",
            });
        }
    };
    
    return (
        <div className="space-y-6">
            <PatientHeader />
            <VitalsBar />
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
                <div className="lg:col-span-2">
                    <ClinicalDataForm form={form} />
                </div>
                <div>
                    <AiActions onAction={handleAiAction} />
                </div>
            </div>

            <AiModal
                isOpen={modalState.open}
                onClose={() => setModalState(s => ({ ...s, open: false }))}
                title={modalState.title}
                content={modalState.content}
                isLoading={modalState.isLoading}
            />
        </div>
    );
}
