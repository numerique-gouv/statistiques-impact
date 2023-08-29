import Progress from '@ramonak/react-progress-bar';

function ProgressBar(props: { progress: number }) {
    return (
        <Progress
            completed={props.progress}
            borderRadius="4px"
            labelSize="12px"
            width="200px"
            bgColor="#000091"
        />
    );
}

export { ProgressBar };
