"use client";

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Loader2 } from "lucide-react";

interface AiModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  content: string;
  isLoading: boolean;
}

export function AiModal({ isOpen, onClose, title, content, isLoading }: AiModalProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-2xl">
        <DialogHeader>
          <DialogTitle className="font-headline text-secondary-foreground">{title}</DialogTitle>
          <DialogDescription>
            This content is AI-generated. Please review carefully.
          </DialogDescription>
        </DialogHeader>
        <ScrollArea className="h-[60vh] p-4 border rounded-md bg-muted/50">
            {isLoading ? (
                <div className="flex items-center justify-center h-full">
                    <Loader2 className="w-8 h-8 animate-spin text-primary" />
                    <p className="ml-2">AI is thinking...</p>
                </div>
            ) : (
                <pre className="text-sm whitespace-pre-wrap font-body">{content}</pre>
            )}
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}
