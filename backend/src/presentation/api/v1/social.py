from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories import (
    FollowRepositoryImpl,
    TrainingReactionRepositoryImpl,
    TrainingCommentRepositoryImpl,
    UserRepositoryImpl,
    TrainingRepositoryImpl,
)
from src.application.use_cases.social.follow_user import FollowUserUseCase
from src.application.use_cases.social.unfollow_user import UnfollowUserUseCase
from src.application.use_cases.social.get_followers import GetFollowersUseCase
from src.application.use_cases.social.get_following import GetFollowingUseCase
from src.application.use_cases.social.search_users import SearchUsersUseCase
from src.application.use_cases.social.approve_follow_request import ApproveFollowRequestUseCase
from src.application.use_cases.social.reject_follow_request import RejectFollowRequestUseCase
from src.application.use_cases.social.get_user_profile import GetUserProfileUseCase
from src.application.use_cases.social.get_user_trainings import GetUserTrainingsUseCase
from src.application.use_cases.social.add_reaction import AddReactionUseCase
from src.application.use_cases.social.remove_reaction import RemoveReactionUseCase
from src.application.use_cases.social.get_training_reactions import GetTrainingReactionsUseCase
from src.application.use_cases.social.add_comment import AddCommentUseCase
from src.application.use_cases.social.delete_comment import DeleteCommentUseCase
from src.application.use_cases.social.get_training_comments import GetTrainingCommentsUseCase
from src.domain.entities.training_reaction import ReactionType
from src.presentation.api.dependencies import get_current_user_id
from src.presentation.schemas.social_schemas import (
    FollowResponse,
    ReactionRequest,
    ReactionResponse,
    CommentRequest,
    CommentResponse,
)
from src.presentation.schemas.auth_schemas import UserResponse
from src.presentation.schemas.training_schemas import TrainingResponse

router = APIRouter(prefix="/social", tags=["social"])


def get_follow_repository(db: Session = Depends(get_db)) -> FollowRepositoryImpl:
    """Dependency to get follow repository."""
    return FollowRepositoryImpl(db)


def get_reaction_repository(db: Session = Depends(get_db)) -> TrainingReactionRepositoryImpl:
    """Dependency to get reaction repository."""
    return TrainingReactionRepositoryImpl(db)


def get_comment_repository(db: Session = Depends(get_db)) -> TrainingCommentRepositoryImpl:
    """Dependency to get comment repository."""
    return TrainingCommentRepositoryImpl(db)


def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    """Dependency to get user repository."""
    return UserRepositoryImpl(db)


def get_training_repository(db: Session = Depends(get_db)) -> TrainingRepositoryImpl:
    """Dependency to get training repository."""
    return TrainingRepositoryImpl(db)


@router.post("/follow/{user_id}", response_model=FollowResponse, status_code=status.HTTP_201_CREATED)
async def follow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Follow a user."""
    follow_repository = get_follow_repository(db)
    use_case = FollowUserUseCase(follow_repository)

    try:
        result = use_case.execute(current_user_id, user_id)
        return FollowResponse(
            id=result.id,
            follower_id=result.follower_id,
            following_id=result.following_id,
            status=result.status.value,
            created_at=result.created_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/follow/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Unfollow a user."""
    follow_repository = get_follow_repository(db)
    use_case = UnfollowUserUseCase(follow_repository)

    try:
        use_case.execute(current_user_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/followers", response_model=List[FollowResponse])
async def get_followers(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get followers of current user."""
    follow_repository = get_follow_repository(db)
    user_repository = get_user_repository(db)
    use_case = GetFollowersUseCase(follow_repository)

    results = use_case.execute(current_user_id)
    response_list = []
    for r in results:
        # Get follower username
        follower_user = user_repository.get_by_id(r.follower_id)
        follower_username = follower_user.username if follower_user else None
        
        response_list.append(
            FollowResponse(
                id=r.id,
                follower_id=r.follower_id,
                following_id=r.following_id,
                status=r.status.value,
                created_at=r.created_at,
                follower_username=follower_username,
            )
        )
    return response_list


@router.get("/following", response_model=List[FollowResponse])
async def get_following(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get users that current user is following."""
    follow_repository = get_follow_repository(db)
    user_repository = get_user_repository(db)
    use_case = GetFollowingUseCase(follow_repository)

    results = use_case.execute(current_user_id)
    response_list = []
    for r in results:
        # Get following username
        following_user = user_repository.get_by_id(r.following_id)
        following_username = following_user.username if following_user else None
        
        response_list.append(
            FollowResponse(
                id=r.id,
                follower_id=r.follower_id,
                following_id=r.following_id,
                status=r.status.value,
                created_at=r.created_at,
                following_username=following_username,
            )
        )
    return response_list


@router.post("/follow/{user_id}/approve", response_model=FollowResponse)
async def approve_follow_request(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Approve a follow request (user_id is the follower who sent the request)."""
    follow_repository = get_follow_repository(db)
    user_repository = get_user_repository(db)
    use_case = ApproveFollowRequestUseCase(follow_repository)

    try:
        result = use_case.execute(user_id, current_user_id)
        # Get follower username
        follower_user = user_repository.get_by_id(result.follower_id)
        follower_username = follower_user.username if follower_user else None
        
        return FollowResponse(
            id=result.id,
            follower_id=result.follower_id,
            following_id=result.following_id,
            status=result.status.value,
            created_at=result.created_at,
            follower_username=follower_username,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/follow/{user_id}/reject", response_model=FollowResponse)
async def reject_follow_request(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Reject a follow request (user_id is the follower who sent the request)."""
    follow_repository = get_follow_repository(db)
    user_repository = get_user_repository(db)
    use_case = RejectFollowRequestUseCase(follow_repository)

    try:
        result = use_case.execute(user_id, current_user_id)
        # Get follower username
        follower_user = user_repository.get_by_id(result.follower_id)
        follower_username = follower_user.username if follower_user else None
        
        return FollowResponse(
            id=result.id,
            follower_id=result.follower_id,
            following_id=result.following_id,
            status=result.status.value,
            created_at=result.created_at,
            follower_username=follower_username,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/users/{user_id}/profile", response_model=UserResponse)
async def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get user profile (requires approved follow relationship)."""
    user_repository = get_user_repository(db)
    follow_repository = get_follow_repository(db)
    use_case = GetUserProfileUseCase(user_repository, follow_repository)

    try:
        result = use_case.execute(user_id, current_user_id)
        return UserResponse(**result.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get("/users/{user_id}/trainings", response_model=List[TrainingResponse])
async def get_user_trainings(
    user_id: int,
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get user trainings (requires approved follow relationship)."""
    from src.presentation.api.v1.trainings import dto_to_response
    
    training_repository = get_training_repository(db)
    follow_repository = get_follow_repository(db)
    use_case = GetUserTrainingsUseCase(training_repository, follow_repository)

    try:
        results = use_case.execute(user_id, current_user_id, start_date, end_date)
        return [dto_to_response(dto) for dto in results]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get("/users/search", response_model=List[UserResponse])
async def search_users(
    q: str = Query(..., min_length=1, description="Search query for username"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Search users by username."""
    user_repository = get_user_repository(db)
    use_case = SearchUsersUseCase(user_repository)

    users = use_case.execute(username_query=q, limit=limit, exclude_user_id=current_user_id)
    return [UserResponse(**user.__dict__) for user in users]


@router.post("/trainings/{training_id}/reactions", response_model=ReactionResponse, status_code=status.HTTP_201_CREATED)
async def add_reaction(
    training_id: int,
    request: ReactionRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Add a reaction to a training."""
    reaction_repository = get_reaction_repository(db)
    use_case = AddReactionUseCase(reaction_repository)

    try:
        reaction_type = ReactionType(request.reaction_type)
        result = use_case.execute(training_id, current_user_id, reaction_type)
        return ReactionResponse(
            id=result.id,
            training_id=result.training_id,
            user_id=result.user_id,
            reaction_type=result.reaction_type.value,
            created_at=result.created_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/trainings/{training_id}/reactions", status_code=status.HTTP_204_NO_CONTENT)
async def remove_reaction(
    training_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Remove a reaction from a training."""
    reaction_repository = get_reaction_repository(db)
    use_case = RemoveReactionUseCase(reaction_repository)

    try:
        use_case.execute(training_id, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/trainings/{training_id}/reactions", response_model=List[ReactionResponse])
async def get_training_reactions(
    training_id: int,
    db: Session = Depends(get_db),
):
    """Get all reactions for a training."""
    reaction_repository = get_reaction_repository(db)
    use_case = GetTrainingReactionsUseCase(reaction_repository)

    results = use_case.execute(training_id)
    return [
        ReactionResponse(
            id=r.id,
            training_id=r.training_id,
            user_id=r.user_id,
            reaction_type=r.reaction_type.value,
            created_at=r.created_at,
        )
        for r in results
    ]


@router.post("/trainings/{training_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    training_id: int,
    request: CommentRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Add a comment to a training."""
    comment_repository = get_comment_repository(db)
    user_repository = get_user_repository(db)
    use_case = AddCommentUseCase(comment_repository)

    try:
        result = use_case.execute(training_id, current_user_id, request.text)
        # Get username
        user = user_repository.get_by_id(current_user_id)
        username = user.username if user else None

        return CommentResponse(
            id=result.id,
            training_id=result.training_id,
            user_id=result.user_id,
            username=username,
            text=result.text,
            created_at=result.created_at,
            updated_at=result.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/trainings/{training_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    training_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Delete a comment."""
    comment_repository = get_comment_repository(db)
    use_case = DeleteCommentUseCase(comment_repository)

    try:
        use_case.execute(comment_id, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/trainings/{training_id}/comments", response_model=List[CommentResponse])
async def get_training_comments(
    training_id: int,
    db: Session = Depends(get_db),
):
    """Get all comments for a training."""
    comment_repository = get_comment_repository(db)
    user_repository = get_user_repository(db)
    use_case = GetTrainingCommentsUseCase(comment_repository)

    results = use_case.execute(training_id)
    comments = []
    for r in results:
        user = user_repository.get_by_id(r.user_id)
        username = user.username if user else None
        comments.append(
            CommentResponse(
                id=r.id,
                training_id=r.training_id,
                user_id=r.user_id,
                username=username,
                text=r.text,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
        )
    return comments


