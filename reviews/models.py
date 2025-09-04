from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone
import uuid

from products.models import Category

class Review(models.Model):
    """
    Review model for products/services
    """
    RATING_CHOICES = [
        (1, '1 Star - Poor'),
        (2, '2 Stars - Fair'), 
        (3, '3 Stars - Good'),
        (4, '4 Stars - Very Good'),
        (5, '5 Stars - Excellent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        max_length=200,
        verbose_name="Review Title",
        help_text="Brief title for your review"
    )
    content = models.TextField(
        verbose_name="Review Content",
        help_text="Detail review content"
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="rating",
        help_text="Rate from 1 to 5 stars"
    )
    
    # Relacionamentos
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Author"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name="Category",
        help_text="Category of the reviewed item"
    )
    
    
    # Campos adicionais
    product_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Product/Service Name",
        help_text="Name of the reviewed product or services"
    )
    pros = models.TextField(
        blank=True,
        verbose_name="Pros",
        help_text="What you liked about it"
    )
    cons = models.TextField(
        blank=True,
        verbose_name="Cons",
        help_text="What could be improved"
    )
    would_recommend = models.BooleanField(
        default=True,
        verbose_name="Would Recommend",
        help_text="Would you recommend this to orders"
    )
    
    # Status e moderação
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Status"
    )
    is_feature = models.BooleanField(
        default=False,
        verbose_name="Feature Review",
        help_text="Mark as feature review"
    )
    
    # Campos de controle
    help_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Helpful Votes"
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Views Count"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Review Date",
        help_text="When the product/service was actually used"
    )
    
    class Meta:
        db_table = 'review'
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['rating']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]
        
    def __str__(self):
        return f"{self.title} - {self.rating}* by {self.author.username}"
    
    def get_absolute_url(self):
        return reverse('review-detail', kwargs={'pk': self.pk})
    
    @property
    def is_approved(self):
        return self.status == 'approved'
    
    @property
    def rating_stars(self):
        """Retuns rating as stars string"""
        return '⭐' * self.rating + '☆' * (5 - self.rating)
    
    def increment_helpful(self):
        """Increment helpful count"""
        self.help_count += 1
        self.save(update_fields=['help_count'])
        
    def increment_views(self):
        """Increment views count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
        
class ReviewImage(models.Model):
    """
    Images attached to reviews
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Review"
    )
    image = models.ImageField(
        upload_to='reviews/images/',
        verbose_name="Image"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Caption"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'review_image'
        verbose_name = "Review Image",
        verbose_name_plural = "Review Images"
        ordering = ['uploaded_at']
        
    def __str__(self):
        return f"image for {self.review.title}"
    
    
class ReviewVote(models.Model):
    """
    Track helpful votes for reviews
    """
    VOTE_CHOICES = [
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
    ]
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="review_votes"
    )
    vote_type = models.CharField(
        max_length=11,
        choices=VOTE_CHOICES,
        verbose_name="Vote Type"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'review_vote'
        verbose_name = "Review Vote"
        verbose_name_plural = "Review Votes"
        unique_together = ['review', 'user'] # one vote per user per review
        
    def __str__(self):
        return F"{self.user.username} - {self.vote_type} on {self.review.title}"
    

class ReviewResponse(models.Model):
    """
    Response from business/admin to reviews
    """
    review = models.OneToOneField(
        Review,
        on_delete=models.CASCADE,
        related_name='response',
        verbose_name='Review'
    )
    responder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review_responses',
        verbose_name='Responder'
    )
    content = models.TextField(
        verbose_name="Response Content"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'review_response'
        verbose_name = "Review Response"
        verbose_name_plural = "Revivew Responses"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Response to {self.review.title}"
    