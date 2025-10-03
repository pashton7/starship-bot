CREATE TABLE IF NOT EXISTS `moderations` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `moderator_id` varchar(20) NOT NULL,
  `moderation_type` varchar(20) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);