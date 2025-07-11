"use client";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Bot, Lightbulb, Stethoscope, FilePlus, Database } from "lucide-react";
import type { AiActionType } from './dashboard';

interface AiActionsProps {
  onAction: (action: AiActionType) => void;
}

export function AiActions({ onAction }: AiActionsProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="font-headline text-secondary-foreground">AI Actions</CardTitle>
        <CardDescription>Use AI to assist with clinical tasks.</CardDescription>
      </CardHeader>
      <CardContent className="grid grid-cols-1 gap-3">
        <Button onClick={() => onAction('coding')}><Stethoscope className="mr-2" />Medical Coding</Button>
        <Button onClick={() => onAction('advisory')}><Bot className="mr-2" />AI Advisory</Button>
        <Button onClick={() => onAction('suggestions')}><Lightbulb className="mr-2" />Suggestions</Button>
        <Button onClick={() => onAction('claims')}><Database className="mr-2" />Claims Database</Button>
        <Button onClick={() => onAction('ehr')}><FilePlus className="mr-2" />Generate E-HR</Button>
      </CardContent>
    </Card>
  );
}
