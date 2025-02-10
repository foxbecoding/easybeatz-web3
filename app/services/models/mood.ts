import { type ApiData } from "@/composables/useApi"

export interface Mood {
    pk: string;
    name: string;
    slug: string;
    error?: any;
}

