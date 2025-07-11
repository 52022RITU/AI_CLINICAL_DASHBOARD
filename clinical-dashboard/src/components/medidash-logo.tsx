import { Stethoscope } from 'lucide-react';

export function MedidashLogo() {
  return (
    <div className="flex items-center gap-2 px-2">
      <Stethoscope className="w-8 h-8 text-sidebar-foreground" />
      <h2 className="text-2xl font-bold text-sidebar-foreground font-headline">MediDash AI</h2>
    </div>
  );
}
