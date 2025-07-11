"use client";

import { useEffect, useState } from "react";
import { UseFormReturn } from "react-hook-form";
import * as z from "zod";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

export const clinicalDataSchema = z.object({
  chiefComplaint: z.string().min(1, { message: "Chief complaint is required." }),
  treatmentPlan: z.string().optional(),
  supportingNotes: z.string().optional(),
  medications: z.string().optional(),
  icdCodes: z.string().optional(),
  investigations: z.string().optional(),
});

interface ClinicalDataFormProps {
  form: UseFormReturn<z.infer<typeof clinicalDataSchema>>;
}

export function ClinicalDataForm({ form }: ClinicalDataFormProps) {
  const [currentDate, setCurrentDate] = useState("");

  useEffect(() => {
    setCurrentDate(new Date().toLocaleDateString());
  }, []);

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle className="font-headline text-secondary-foreground">Clinical Data</CardTitle>
        <CardDescription>Enter patient's clinical information. Fields with <span className="text-destructive">*</span> are mandatory.</CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form className="space-y-4">
            <FormField
              control={form.control}
              name="chiefComplaint"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Chief Complaint <span className="text-destructive">*</span></FormLabel>
                  <FormControl>
                    <Textarea placeholder="e.g., Chest pain and shortness of breath..." {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="treatmentPlan"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Treatment Plan</FormLabel>
                  <FormControl>
                    <Textarea placeholder="e.g., Prescribe aspirin, schedule for stress test..." {...field} />
                  </FormControl>
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="supportingNotes"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Supporting Notes</FormLabel>
                  <FormControl>
                    <Textarea placeholder="e.g., Patient has a history of smoking..." {...field} />
                  </FormControl>
                </FormItem>
              )}
            />
             <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField
                    control={form.control}
                    name="medications"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Medications</FormLabel>
                        <FormControl>
                            <Input placeholder="e.g., Aspirin 81mg" {...field} />
                        </FormControl>
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="icdCodes"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>ICD Codes</FormLabel>
                        <FormControl>
                            <Input placeholder="e.g., I25.10" {...field} />
                        </FormControl>
                        </FormItem>
                    )}
                />
            </div>
            <FormField
                control={form.control}
                name="investigations"
                render={({ field }) => (
                    <FormItem>
                    <FormLabel>Investigations</FormLabel>
                    <FormControl>
                        <Textarea placeholder="e.g., ECG, Blood tests..." {...field} />
                    </FormControl>
                    </FormItem>
                )}
            />
             <div>
                <h4 className="text-sm font-medium text-muted-foreground mt-6 mb-2">Doctor Details (Auto-filled)</h4>
                <div className="text-sm p-3 bg-muted/50 rounded-md space-y-1">
                    <p><strong>Doctor:</strong> Dr. Smith</p>
                    <p><strong>Specialty:</strong> Cardiology</p>
                    <p><strong>Date:</strong> {currentDate}</p>
                </div>
            </div>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
