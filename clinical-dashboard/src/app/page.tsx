import { SidebarProvider, Sidebar, SidebarInset, SidebarTrigger, SidebarHeader, SidebarContent, SidebarFooter } from "@/components/ui/sidebar";
import Dashboard from "@/components/dashboard";
import { MedidashLogo } from "@/components/medidash-logo";
import { SidebarNav } from "@/components/sidebar-nav";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { LogOut } from "lucide-react";

export default function Home() {
  return (
    <SidebarProvider>
      <Sidebar>
        <SidebarHeader>
          <MedidashLogo />
        </SidebarHeader>
        <SidebarContent>
          <SidebarNav />
        </SidebarContent>
        <SidebarFooter>
            <div className="flex items-center gap-3 p-2">
                <Avatar className="h-10 w-10">
                    <AvatarImage src="https://placehold.co/40x40.png" alt="@dr-smith" data-ai-hint="doctor avatar" />
                    <AvatarFallback>DS</AvatarFallback>
                </Avatar>
                <div className="flex flex-col text-sm text-sidebar-foreground truncate">
                    <span className="font-semibold">Dr. Smith</span>
                    <span className="text-xs text-sidebar-foreground/70">Cardiologist</span>
                </div>
                <Button variant="ghost" size="icon" className="ml-auto text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground">
                    <LogOut className="h-5 w-5" />
                </Button>
            </div>
        </SidebarFooter>
      </Sidebar>
      <SidebarInset>
        <header className="flex items-center justify-between p-4 border-b bg-background sticky top-0 z-10">
            <div className="flex items-center gap-2">
                <SidebarTrigger className="md:hidden" />
                <h1 className="text-3xl font-bold font-headline text-secondary-foreground">Dashboard</h1>
            </div>
        </header>
        <main className="p-4 lg:p-6">
          <Dashboard />
        </main>
      </SidebarInset>
    </SidebarProvider>
  );
}
