import { z } from "zod";

export const messageSchema = z.object({
    role: z.enum(['User', 'Assistant','System']), 
    content: z.string()
})

export type Message = z.infer<typeof messageSchema>