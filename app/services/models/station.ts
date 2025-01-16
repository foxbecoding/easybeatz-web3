import type { ApiData } from "@/composables/useApi"

export interface Station {
    created: string;
    description: string | null;
    email: string | null;
    handle: string | null;
    is_owner: boolean;
    name: string | null;
} 
