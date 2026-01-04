import ReactionButton from './ReactionButton'

interface ReactionListProps {
  trainingId: number
  onUpdate?: () => void
}

export default function ReactionList({ trainingId, onUpdate }: ReactionListProps) {
  return (
    <div className="flex items-center gap-2 flex-wrap">
      <ReactionButton trainingId={trainingId} reactionType="LIKE" onUpdate={onUpdate} />
      <ReactionButton trainingId={trainingId} reactionType="LOVE" onUpdate={onUpdate} />
      <ReactionButton trainingId={trainingId} reactionType="FIRE" onUpdate={onUpdate} />
      <ReactionButton trainingId={trainingId} reactionType="MUSCLE" onUpdate={onUpdate} />
      <ReactionButton trainingId={trainingId} reactionType="TARGET" onUpdate={onUpdate} />
    </div>
  )
}


