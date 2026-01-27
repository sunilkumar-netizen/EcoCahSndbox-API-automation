#!/bin/bash

###############################################################################
# Docker Test Runner
# Run tests in Docker container
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Default values
ENV="${ENV:-qa}"
TAGS="${TAGS:-smoke}"
BUILD=false

echo -e "${BLUE}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Docker API Test Runner                         ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════╝${NC}"
echo ""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--env)
            ENV="$2"
            shift 2
            ;;
        -t|--tags)
            TAGS="$2"
            shift 2
            ;;
        -b|--build)
            BUILD=true
            shift
            ;;
        -h|--help)
            echo "Usage: ./docker_run.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -e, --env <ENV>     Environment: dev, qa, uat (default: qa)"
            echo "  -t, --tags <TAGS>   Tags to run (default: smoke)"
            echo "  -b, --build         Rebuild Docker image"
            echo "  -h, --help          Show help"
            echo ""
            echo "Examples:"
            echo "  ./docker_run.sh -e qa -t smoke"
            echo "  ./docker_run.sh --env uat --tags payments --build"
            exit 0
            ;;
        *)
            echo -e "${YELLOW}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}Configuration:${NC}"
echo -e "  Environment: ${YELLOW}$ENV${NC}"
echo -e "  Tags: ${YELLOW}$TAGS${NC}"
echo ""

# Build image if requested
if [ "$BUILD" = true ]; then
    echo -e "${BLUE}Building Docker image...${NC}"
    docker-compose build
    echo ""
fi

# Run tests
echo -e "${BLUE}Running tests in Docker...${NC}"
ENV=$ENV TAGS=$TAGS docker-compose up --abort-on-container-exit api-tests

# Get exit code
EXIT_CODE=$?

# Cleanup
docker-compose down

# Show results
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Tests completed successfully!${NC}"
else
    echo -e "${YELLOW}⚠️  Some tests failed (exit code: $EXIT_CODE)${NC}"
fi

echo ""
echo -e "${BLUE}Reports available in: ./reports/${NC}"
echo -e "${BLUE}Logs available in: ./logs/${NC}"
echo ""

exit $EXIT_CODE
