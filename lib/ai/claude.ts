import Anthropic from '@anthropic-ai/sdk'

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
})

export const MODEL = 'claude-opus-4-6'

export interface FaultSearchResult {
  diagnosis: string
  likely_causes: string[]
  recommended_steps: string[]
  safety_notes: string[]
  related_procedures: string[]
  confidence: 'high' | 'medium' | 'low'
}

export interface SearchContext {
  query: string
  site?: string
  procedureContext?: string
  documentContext?: string
}

/**
 * Run an AI-powered fault diagnosis search.
 */
export async function searchFault(context: SearchContext): Promise<FaultSearchResult> {
  const systemPrompt = `You are an expert industrial maintenance engineer AI assistant.
Your role is to help engineers diagnose equipment faults and find resolution procedures.

When given a fault description or symptom, respond with a structured JSON analysis containing:
- A clear diagnosis of the likely fault
- The most probable causes (ordered by likelihood)
- Step-by-step recommended resolution actions
- Safety notes and warnings
- Related procedure names to look up
- Your confidence level

Always prioritise safety. If the fault could be dangerous, lead with safety notes.
Be concise, technical, and actionable.`

  const userContent = [
    `Fault query: ${context.query}`,
    context.site ? `Site: ${context.site}` : null,
    context.procedureContext ? `Relevant procedures context:\n${context.procedureContext}` : null,
    context.documentContext ? `Relevant documentation:\n${context.documentContext}` : null,
  ]
    .filter(Boolean)
    .join('\n\n')

  const message = await anthropic.messages.create({
    model: MODEL,
    max_tokens: 1024,
    system: systemPrompt,
    messages: [
      {
        role: 'user',
        content: userContent,
      },
    ],
  })

  const content = message.content[0]
  if (content.type !== 'text') {
    throw new Error('Unexpected response type from Claude')
  }

  // Extract JSON from response (Claude may wrap in markdown code blocks)
  const jsonMatch = content.text.match(/```(?:json)?\s*([\s\S]*?)\s*```/) ||
    content.text.match(/(\{[\s\S]*\})/)

  if (!jsonMatch) {
    // Fallback: structure the plain text response
    return {
      diagnosis: content.text,
      likely_causes: [],
      recommended_steps: [],
      safety_notes: [],
      related_procedures: [],
      confidence: 'medium',
    }
  }

  try {
    return JSON.parse(jsonMatch[1] ?? jsonMatch[0]) as FaultSearchResult
  } catch {
    return {
      diagnosis: content.text,
      likely_causes: [],
      recommended_steps: [],
      safety_notes: [],
      related_procedures: [],
      confidence: 'medium',
    }
  }
}

/**
 * Stream a fault search response for real-time UI updates.
 */
export async function streamFaultSearch(
  context: SearchContext,
  onChunk: (text: string) => void
): Promise<void> {
  const stream = await anthropic.messages.stream({
    model: MODEL,
    max_tokens: 2048,
    system: `You are an expert industrial maintenance engineer AI assistant helping diagnose equipment faults and find resolution procedures. Be concise, technical, and prioritise safety.`,
    messages: [
      {
        role: 'user',
        content: `Diagnose this fault and provide resolution steps:\n\n${context.query}${
          context.site ? `\n\nSite: ${context.site}` : ''
        }`,
      },
    ],
  })

  for await (const chunk of stream) {
    if (
      chunk.type === 'content_block_delta' &&
      chunk.delta.type === 'text_delta'
    ) {
      onChunk(chunk.delta.text)
    }
  }
}
